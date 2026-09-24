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


from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction

from sales.models.sale import Sale
from sales.models.sale_item import SaleItem
from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm

from inventory.integration import update_inventory_from_sale, revert_inventory_from_sale
from accounting.services import AccountingService
from accounting.utils.period_validation import (
    get_open_period_for_date,
    NoOpenPeriodError,
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
        return redirect("sales:sale_detail", pk=sale.pk)

    if not sale.items.exists():
        messages.error(request, "No se puede emitir una venta sin ítems cargados.")
        return redirect("sales:sale_detail", pk=sale.pk)

    try:
        with transaction.atomic():
            # 1. Recalcular subtotales
            sale.recalc_totals()

            # 2. Descontar stock de inventario y generar el asiento contable
            update_inventory_from_sale(sale)
            AccountingService.post_sale(sale)

            # 3. Cambiar estado a emitida
            sale.status = "ISSUED"
            sale.save(update_fields=["status"])

        messages.success(request, f"Venta N° {sale.number} emitida y contabilizada correctamente.")

    except Exception as e:
        messages.error(request, f"Error al emitir la venta: {str(e)}")

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

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone

from sales.models.sale import Sale
from fiscal.models import ElectronicVoucherBook, FiscalInvoice, FiscalInvoiceLine
from inventory.integration import update_inventory_from_sale
from accounting.services import AccountingService


def get_voucher_type_for_customer(customer):
    """Determina la clave de comprobante (FA, FB, FC) según perfil fiscal AFIP."""
    profile = getattr(customer, "tax_profile", None)
    category = getattr(profile, "afip_category", "CF") if profile else "CF"

    if category == "RI":
        return "FA"
    elif category == "CF":
        return "FB"
    else:
        return "FC"


@login_required
@require_POST
def issue_sale(request, pk):
    company_id = request.session.get("active_company_id")
    sale = get_object_or_404(Sale, pk=pk, company_id=company_id)

    # 1. Validar estado y existencia de ítems
    if sale.status != "DRAFT":
        messages.warning(request, "La venta ya fue emitida anteriormente.")
        return redirect("sales:sale_detail", pk=sale.pk)

    if not sale.items.exists():
        messages.error(request, "No se puede emitir una venta sin ítems.")
        return redirect("sales:sale_detail", pk=sale.pk)

    try:
        with transaction.atomic():
            # 2. Recalcular subtotales comerciales
            sale.recalc_totals()

            # 3. Determinar tipo de comprobante según el cliente
            voucher_type = get_voucher_type_for_customer(sale.customer)
            point_of_sale = 1  # Punto de Venta activo por defecto

            # 4. Obtener el talonario de la empresa
            voucher_book = ElectronicVoucherBook.objects.filter(
                company=sale.company,
                point_of_sale=point_of_sale,
                voucher_type=voucher_type,
                enabled=True,
            ).first()

            if not voucher_book:
                raise ValueError(
                    f"No existe un talonario habilitado para {voucher_type} en el Punto de Venta {point_of_sale}."
                )

            # 5. Crear la cabecera del comprobante fiscal
            fiscal_invoice = FiscalInvoice.objects.create(
                company=sale.company,
                point_of_sale=point_of_sale,
                voucher_book=voucher_book,
                date=sale.date or timezone.now().date(),
                customer_name=sale.customer.name,
                customer_tax_id=getattr(sale.customer, "tax_id", "") or "",
            )

            # 6. Copiar los ítems a la factura fiscal
            for item in sale.items.all():
                FiscalInvoiceLine.objects.create(
                    invoice=fiscal_invoice,
                    company=sale.company,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    tax=item.tax,
                )

            # 7. Finalizar el comprobante (obtiene número de voucher_book y CAE de AFIP)
            fiscal_invoice.finalize()

            # 8. Descontar stock y registrar el asiento en la contabilidad
            update_inventory_from_sale(sale)
            AccountingService.post_sale(sale)

            # 9. Cambiar el estado comercial a emitida
            sale.status = "ISSUED"
            sale.save(update_fields=["status"])

        messages.success(
            request,
            f"Venta N° {sale.number} emitida con éxito. Comprobante Fiscal N° {fiscal_invoice.number} (CAE: {fiscal_invoice.cae})."
        )

    except Exception as e:
        messages.error(request, f"Error al emitir la factura: {str(e)}")

    return redirect("sales:sale_detail", pk=sale.pk)