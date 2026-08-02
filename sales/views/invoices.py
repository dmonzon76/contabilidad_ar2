from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.middleware.active_company import get_active_company_from_request

from sales.models.invoice import Invoice
from sales.forms.invoice import InvoiceForm
from sales.forms.invoice_line import InvoiceLineFormSet

from fiscal.utils.invoice_type import determine_invoice_type
from fiscal.utils.iva import calculate_iva
from fiscal.utils.iibb import calculate_iibb
from fiscal.utils.perceptions import calculate_perceptions, calculate_retentions

from inventory.models import InventoryItem, InventoryMovement

from accounting.models.journal import JournalEntry, JournalEntryLine
from accounting.utils import get_account


@login_required
def invoice_create(request):
    company = get_active_company_from_request(request)

    if request.method == "POST":
        form = InvoiceForm(request.POST, company=company)
        formset = InvoiceLineFormSet(request.POST, company=company)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.company = company

            # ---------------------------------------------------------
            # TIPO DE COMPROBANTE (A/B/C)
            # ---------------------------------------------------------
            invoice_type = determine_invoice_type(invoice.customer)
            invoice.series.code = invoice_type
            invoice.series.save()

            # ---------------------------------------------------------
            # NUMERACIÓN AUTOMÁTICA
            # ---------------------------------------------------------
            invoice.number = invoice.series.next_number
            invoice.series.next_number += 1
            invoice.series.save()

            invoice.save()

            # ---------------------------------------------------------
            # GUARDAR LÍNEAS
            # ---------------------------------------------------------
            formset.instance = invoice
            lines = formset.save()

            # ---------------------------------------------------------
            # CÁLCULO FISCAL AUTOMÁTICO
            # ---------------------------------------------------------
            subtotal, iva_total = calculate_iva(lines)
            iibb_total = calculate_iibb(invoice.customer, subtotal)
            perception_total = calculate_perceptions(invoice.customer, subtotal)
            retention_total = calculate_retentions(invoice.customer, subtotal)

            invoice.subtotal = subtotal
            invoice.vat_amount = iva_total
            invoice.total = (
                subtotal
                + iva_total
                + iibb_total
                + perception_total
                - retention_total
            )

            invoice.save()

            # ---------------------------------------------------------
            # INTEGRACIÓN DE STOCK + KARDEX (CORRECTA)
            # ---------------------------------------------------------
            for line in lines:
                if line.product:
                    # Obtener el item de inventario asociado al producto
                    try:
                        item = InventoryItem.objects.get(product=line.product)
                    except InventoryItem.DoesNotExist:
                        item = InventoryItem.objects.create(
                            product=line.product,
                            quantity=0,
                            min_stock=0
                        )

                    # Control opcional de stock negativo
                    if item.quantity < line.quantity:
                        pass  # si querés bloquear la venta, acá va el return

                    # Descontar stock
                    item.quantity -= line.quantity
                    item.save()

                    # Registrar movimiento (Kardex)
                    InventoryMovement.objects.create(
                        item=item,
                        movement_type="OUT",
                        quantity=line.quantity,
                        note=f"Venta – Factura {invoice.series.code}-{invoice.number}",
                    )

            # ---------------------------------------------------------
            # ASIENTO CONTABLE AUTOMÁTICO
            # ---------------------------------------------------------
            entry = JournalEntry.objects.create(
                company=company,
                date=invoice.date,
                description=f"Factura {invoice.series.code}-{invoice.number}",
            )

            # 1) Cliente (Debe)
            JournalEntryLine.objects.create(
                entry=entry,
                account=get_account("110101"),  # Clientes
                debit=invoice.total,
                credit=0,
            )

            # 2) Ventas + IVA según líneas
            for line in lines:
                line_subtotal = line.quantity * line.unit_price
                vat_amount = line_subtotal * (line.vat_rate / 100)

                # Ventas según alícuota
                if line.vat_rate == 21:
                    sales_account = get_account("410101")
                elif line.vat_rate == 10.5:
                    sales_account = get_account("410102")
                elif line.vat_rate == 27:
                    sales_account = get_account("410103")
                elif line.vat_rate == 0:
                    sales_account = get_account("410201")
                else:
                    sales_account = get_account("410301")

                JournalEntryLine.objects.create(
                    entry=entry,
                    account=sales_account,
                    debit=0,
                    credit=line_subtotal,
                )

                # IVA Débito Fiscal
                if vat_amount > 0:
                    JournalEntryLine.objects.create(
                        entry=entry,
                        account=get_account("210101"),
                        debit=0,
                        credit=vat_amount,
                    )

            # 3) IIBB
            if iibb_total > 0:
                JournalEntryLine.objects.create(
                    entry=entry,
                    account=get_account("210201"),
                    debit=0,
                    credit=iibb_total,
                )

            # 4) Percepciones
            if perception_total > 0:
                JournalEntryLine.objects.create(
                    entry=entry,
                    account=get_account("210301"),
                    debit=0,
                    credit=perception_total,
                )

            # 5) Retenciones
            if retention_total > 0:
                JournalEntryLine.objects.create(
                    entry=entry,
                    account=get_account("210302"),
                    debit=retention_total,
                    credit=0,
                )

            return redirect("sales:invoice_detail", invoice_id=invoice.id)

    else:
        form = InvoiceForm(company=company)
        formset = InvoiceLineFormSet(company=company)

    return render(
        request,
        "sales/invoices/create.html",
        {
            "company": company,
            "form": form,
            "formset": formset,
        },
    )


@login_required
def invoice_detail(request, invoice_id):
    company = get_active_company_from_request(request)
    invoice = get_object_or_404(Invoice, id=invoice_id, company=company)

    return render(
        request,
        "sales/invoices/detail.html",
        {
            "company": company,
            "invoice": invoice,
        },
    )
