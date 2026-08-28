from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from fiscal.models.fiscal_invoice import FiscalInvoice
from sales.models.sale import Sale

from accounting.services.generate_entry import generate_accounting_entry

from core.utils.company_active import get_active_company
from core.utils.company_access import user_has_access


@login_required
@permission_required("fiscal.add_fiscalinvoice", raise_exception=True)
@require_POST
def fiscal_invoice_create(request, sale_id):

    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    sale = get_object_or_404(Sale, id=sale_id, company=company)

    # Evitar duplicación de factura fiscal
    if hasattr(sale, "fiscal_invoice"):
        return redirect("sales:sale_detail", pk=sale.id)

    voucher_type = "B"
    point_of_sale = 1

    voucher_number = FiscalInvoice.next_number(
        company=company,
        point_of_sale=point_of_sale,
        voucher_type=voucher_type
    )

    invoice = FiscalInvoice.objects.create(
        company=company,
        customer=sale.customer,
        sale=sale,
        voucher_type=voucher_type,
        point_of_sale=point_of_sale,
        voucher_number=voucher_number,
    )

    # Finaliza la factura (totales + CAE)
    invoice.finalize()

    # Genera asiento contable automático basado en Tax.account_code
    generate_accounting_entry(invoice, request.user)

    return redirect("sales:sale_detail", pk=sale.id)


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_list(request):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoices = FiscalInvoice.objects.filter(company=company)\
        .select_related("customer", "sale")\
        .order_by("-date", "-id")

    return render(request, "fiscal/fiscal_invoice_list.html", {"invoices": invoices})


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_detail(request, pk):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoice = get_object_or_404(FiscalInvoice, pk=pk, company=company)
    return render(request, "fiscal/fiscal_invoice_form.html", {"invoice": invoice})
