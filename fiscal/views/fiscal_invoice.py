from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.utils import timezone

from fiscal.models.fiscal_invoice import FiscalInvoice
from fiscal.models.electronic_voucher_book import ElectronicVoucherBook
from sales.models.sale import Sale

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

    voucher_type = "FA"
    point_of_sale = 1

    voucher_book = ElectronicVoucherBook.objects.filter(
        company=company,
        point_of_sale=point_of_sale,
        voucher_type=voucher_type,
        enabled=True,
    ).first()

    if not voucher_book:
        return HttpResponseForbidden(
            "No active electronic voucher book configured for this company."
        )

    invoice_number = FiscalInvoice.next_number(
        company=company,
        point_of_sale=point_of_sale,
        voucher_type=voucher_type,
    )

    invoice = FiscalInvoice.objects.create(
        company=company,
        voucher_book=voucher_book,
        number=invoice_number,
        date=timezone.now().date(),
        customer_name=sale.customer.name,
        customer_tax_id=getattr(sale.customer, "tax_id", "") or "",
    )

    return redirect("fiscal:fiscal_invoice_detail", pk=invoice.pk)


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_list(request):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoices = (
        FiscalInvoice.objects.filter(company=company)
        .select_related("voucher_book")
        .order_by("-date", "-id")
    )

    return render(request, "fiscal/fiscal_invoice_list.html", {"invoices": invoices})


@login_required
@permission_required("fiscal.view_fiscalinvoice", raise_exception=True)
def fiscal_invoice_detail(request, pk):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    invoice = get_object_or_404(FiscalInvoice, pk=pk, company=company)
    return render(request, "fiscal/fiscal_invoice_form.html", {"invoice": invoice})
