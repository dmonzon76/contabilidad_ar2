from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounting.models import Account
from core.utils.company_access import user_has_access


@login_required
def trial_balance_view(request):
    company = request.active_company

    # Seguridad multi-company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    # Todas las cuentas de la empresa
    accounts = Account.objects.filter(company=company).order_by("code")

    rows = []
    total_debit = 0
    total_credit = 0

    for acc in accounts:
        debit = acc.total_debit(company)
        credit = acc.total_credit(company)

        rows.append({
            "account": acc,
            "debit": debit,
            "credit": credit,
            "balance": debit - credit,
        })

        total_debit += debit
        total_credit += credit

    return render(request, "accounting/trial_balance.html", {
        "company": company,
        "rows": rows,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "is_balanced": total_debit == total_credit,
    })
