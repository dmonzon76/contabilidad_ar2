from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounting.models import Account
from core.utils.company_access import user_has_access


@login_required
def balance_sheet_view(request):
    company = request.active_company

    # Seguridad multi-company
    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    # Filtrar cuentas por tipo IFRS
    assets = Account.objects.filter(company=company, type="ASSET").order_by("code")
    liabilities = Account.objects.filter(company=company, type="LIABILITY").order_by("code")
    equity = Account.objects.filter(company=company, type="EQUITY").order_by("code")

    # Calcular saldos
    def rows_for(accounts):
        rows = []
        total = 0
        for acc in accounts:
            bal = acc.balance(company)
            rows.append({
                "account": acc,
                "balance": bal,
            })
            total += bal
        return rows, total

    asset_rows, total_assets = rows_for(assets)
    liability_rows, total_liabilities = rows_for(liabilities)
    equity_rows, total_equity = rows_for(equity)

    # IFRS: Activo = Pasivo + Patrimonio
    is_balanced = total_assets == (total_liabilities + total_equity)

    return render(request, "accounting/balance_sheet.html", {
        "company": company,
        "asset_rows": asset_rows,
        "liability_rows": liability_rows,
        "equity_rows": equity_rows,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "is_balanced": is_balanced,
    })
