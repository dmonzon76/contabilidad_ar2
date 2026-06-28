from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounting.models import Account, JournalEntryLine
from core.utils.company_access import user_has_access


@login_required
def ledger_view(request, account_id):
    company = request.active_company

    # Seguridad multi-company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    # Cuenta solicitada
    account = get_object_or_404(Account, id=account_id, company=company)

    # Líneas del mayor
    lines = (
        JournalEntryLine.objects
        .filter(account=account, entry__company=company)
        .select_related("entry")
        .order_by("entry__date", "entry__id")
    )

    # Cálculo del saldo acumulado
    running_balance = 0
    ledger_rows = []

    for line in lines:
        running_balance += line.debit - line.credit

        ledger_rows.append({
            "date": line.entry.date,
            "description": line.description or line.entry.description,
            "debit": line.debit,
            "credit": line.credit,
            "balance": running_balance,
            "entry_id": line.entry.id,
        })

    return render(request, "accounting/ledger/view.html", {
        "company": company,
        "account": account,
        "ledger_rows": ledger_rows,
        "final_balance": running_balance,
    })
