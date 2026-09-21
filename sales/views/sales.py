from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST

from sales.models import sale
from sales.models.sale import Sale
from sales.models.sale_item import SaleItem

from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm

from inventory.integration import update_inventory_from_sale, revert_inventory_from_sale

from accounting.services import AccountingService

# VALIDACIÓN CONTABLE
from accounting.utils.period_validation import (
    get_open_period_for_date,
    NoOpenPeriodError,
)

# ============================================================
# LISTA DE VENTAS
# ============================================================


class SaleListView(ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.filter(
            company_id=self.request.session.get("active_company_id")
        )


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
        created_accounts = AccountingService.ensure_required_accounts(company)

        if created_accounts:
            messages.warning(
                self.request,
                "Se creó el plan de cuentas base para la empresa antes de registrar la venta.",
            )

        sale = form.save(commit=False)
        sale.company = company
        sale.save()

        self.object = sale

        return redirect(
            "sales:sale_detail",
            pk=sale.pk,
        )

    def get_success_url(self):
        return reverse_lazy(
            "sales:sale_detail",
            kwargs={"pk": self.object.pk},
        )


# ============================================================
# DETALLE DE VENTA
# ============================================================


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"

    def get_queryset(self):
        return Sale.objects.filter(
            company_id=self.request.session.get("active_company_id")
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
                "sales:sale_detail",
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


@require_POST
def issue_sale(request, pk):
    sale = get_object_or_404(
        Sale,
        pk=pk,
        company_id=request.session.get("active_company_id"),
    )

    if sale.status != "DRAFT":
        messages.warning(request, "Sale already issued.")
        return redirect("sales:sale_detail", pk=sale.pk)

    if not sale.items.exists():
        messages.error(request, "Cannot issue a sale without items.")
        return redirect("sales:sale_detail", pk=sale.pk)

    sale.recalc_totals()
    update_inventory_from_sale(sale)
    AccountingService.post_sale(sale)

    sale.status = "ISSUED"
    sale.save(update_fields=["status"])

    messages.success(request, f"Sale {sale.number} issued successfully.")
    return redirect("sales:sale_detail", pk=sale.pk)


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
            "sales/sale_detail.html",
            {"sale": sale, "error": str(e)},
        )

    sale.delete()

    return redirect("sales:sale_list")
