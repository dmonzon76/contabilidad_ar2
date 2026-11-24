from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from accounting.models import (
    AccountMovement,
    JournalEntry,
)
from accounting.services import AccountingService
from accounting.utils.period_validation import (
    NoOpenPeriodError,
    get_open_period_for_date,
)
from inventory.integration import (
    update_inventory_from_sale,
    validate_inventory_before_issue,
)
from inventory.models import InventoryMovement
from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm
from sales.models.sale import Sale
from sales.models.sale_item import SaleItem

# ============================================================
# LISTA DE VENTAS
# ============================================================

class SaleListView(ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.filter(company_id=self.request.session.get("active_company_id"))


class SaleWorkspaceView(DetailView):
    model = Sale
    template_name = "sales/sale_workspace.html"
    context_object_name = "sale"

    def get_queryset(self):
        return Sale.objects.filter(company_id=self.request.session.get("active_company_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sale = self.object

        context["item_form"] = SaleItemForm(company=sale.company)

        context["journal_entry"] = JournalEntry.objects.filter(source_key=f"sale:{sale.pk}").first()

        context["inventory_movements"] = (
            InventoryMovement.objects.filter(
                sale=sale,
            )
            .select_related(
                "item",
                "item__product",
            )
            .order_by("-date")
        )

        context["customer_movements"] = (
            AccountMovement.objects.filter(
                sale=sale,
            )
            .select_related(
                "customer",
            )
            .order_by("-date")
        )

        context["inventory_movements_count"] = context["inventory_movements"].count()

        context["customer_movements_count"] = context["customer_movements"].count()

        return context


# ============================================================
# CREACIÓN DE VENTA
# ============================================================


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company_id"] = self.request.active_company.id
        return kwargs

    def form_valid(self, form):
        company = self.request.active_company

        sale = form.save(commit=False)
        sale.company = company
        sale.save()

        self.object = sale

        return redirect(
            "sales:sale_workspace",
            pk=sale.pk,
        )

    def get_success_url(self):
        return reverse_lazy(
            "sales:sale_workspace",
            kwargs={"pk": self.object.pk},
        )


# ============================================================
# AGREGAR ÍTEM A LA VENTA
# ============================================================


def sale_item_add(request, sale_id):
    sale = get_object_or_404(
        Sale,
        id=sale_id,
        company_id=request.session.get("active_company_id"),
    )

    try:
        get_open_period_for_date(sale.date)

    except NoOpenPeriodError as e:
        messages.error(
            request,
            f"No se puede agregar items: {e}",
        )

        return render(
            request,
            "sales/sale_item_add.html",
            {
                "sale": sale,
                "error": str(e),
            },
        )

    if request.method == "POST":
        form = SaleItemForm(
            request.POST,
            company=sale.company,
        )

        if form.is_valid():
            item = form.save(commit=False)

            item.sale = sale

            item.save()

            sale.recalc_totals()

            return redirect(
                "sales:sale_workspace",
                pk=sale.id,
            )

        print(form.errors)

    else:
        form = SaleItemForm(
            company=sale.company,
        )

    return render(
        request,
        "sales/sale_item_add.html",
        {
            "form": form,
            "sale": sale,
        },
    )


@login_required
@require_POST
def sale_item_delete(request, pk):
    item = get_object_or_404(
        SaleItem,
        pk=pk,
        sale__company_id=request.session.get("active_company_id"),
    )

    sale = item.sale

    if sale.status != "DRAFT":
        messages.error(request, "Issued sales cannot be modified.")

        return redirect(
            "sales:sale_workspace",
            pk=sale.pk,
        )

    item.delete()

    sale.recalc_totals()

    messages.success(request, "Item deleted successfully.")

    return redirect(
        "sales:sale_workspace",
        pk=sale.pk,
    )


# ... (vistas anteriores) ...


@login_required
@require_POST
def issue_sale(request, pk):
    sale = get_object_or_404(
        Sale,
        pk=pk,
        company_id=request.session.get("active_company_id"),
    )

    if sale.status != "DRAFT":
        messages.warning(request, "La venta ya fue emitida anteriormente.")
        return redirect("sales:sale_workspace", pk=sale.pk)

    if not sale.items.exists():
        messages.error(request, "No se puede emitir una venta sin ítems cargados.")
        return redirect("sales:sale_workspace", pk=sale.pk)

    try:
        with transaction.atomic():
            # 1. Recalcular subtotales
           sale.recalc_totals()

            # Validación previa de inventario
           validate_inventory_before_issue(sale)

            # Descontar stock y contabilizar
           update_inventory_from_sale(sale)
           AccountingService.post_sale(sale)


            # 2. Descontar stock de inventario y generar el asiento contable
           update_inventory_from_sale(sale)
           AccountingService.post_sale(sale)

            # 3. Cambiar estado a emitida
           sale.status = "ISSUED"
           sale.save(update_fields=["status"])

        messages.success(
            request,
            f"Venta N° {sale.number} emitida y contabilizada correctamente.",
        )

    except Exception as e:
        messages.error(request, f"Error al emitir la venta: {str(e)}")

    return redirect("sales:sale_workspace", pk=sale.pk)


# ============================================================
# ELIMINAR VENTA
# ============================================================


def sale_delete(request, pk):
    sale = get_object_or_404(
        Sale,
        pk=pk,
        company_id=request.session.get("active_company_id"),
    )

    # VALIDACIÓN CONTABLE
    try:
        get_open_period_for_date(sale.date)
    except NoOpenPeriodError as e:
        messages.error(
            request,
            f"No se puede eliminar la venta: {str(e)}",
        )
        return render(
            request,
            "sales/sale_workspace.html",
            {"sale": sale, "error": str(e)},
        )

    sale.delete()

    return redirect("sales:sale_list")


def get_voucher_type_for_customer(customer):
    """Determina la clave de comprobante (FA, FB, FC) según perfil fiscal AFIP."""
    profile = getattr(customer, "tax_profile", None)
    category = getattr(profile, "afip_category", "CF") if profile else "CF"

    if category == "RI":
        return "FA"
    if category == "CF":
        return "FB"
    return "FC"


@login_required
def sale_item_edit(request, pk):
    item = get_object_or_404(
        SaleItem,
        pk=pk,
        sale__company_id=request.session.get("active_company_id"),
    )

    sale = item.sale

    if sale.status != "DRAFT":
        messages.error(request, "Issued sales cannot be modified.")

        return redirect(
            "sales:sale_workspace",
            pk=sale.pk,
        )

    if request.method == "POST":
        form = SaleItemForm(
            request.POST,
            instance=item,
            company=sale.company,
        )

        if form.is_valid():
            form.save()

            sale.recalc_totals()

            messages.success(request, "Item updated successfully.")

            return redirect(
                "sales:sale_workspace",
                pk=sale.pk,
            )

    else:
        form = SaleItemForm(
            instance=item,
            company=sale.company,
        )

    return render(
        request,
        "sales/edit_sale_item.html",
        {
            "form": form,
            "item": item,
            "sale": sale,
        },
    )
