from django.urls import path

# Accounts
from accounting.views.account import (
    account_list,
    account_create,
    account_edit,
    account_delete,
    account_add_child,
    period_list,
    period_open,
    period_close,
    period_lock,
)

# Journal
from accounting.views.journal import (
    journal_list,
    journal_create,
)

# Ledger
from accounting.views.ledger import ledger_view

# Trial Balance
from accounting.views.trial_balance import trial_balance_view

# Balance Sheet
from accounting.views.balance_sheet import balance_sheet_view

# Dashboard + Fiscal Years
from accounting.views.dashboard import (
    accounting_dashboard,
    fiscal_year_list,
    fiscal_year_open,
    fiscal_year_close,
)

# NEW: Create Fiscal Year
from accounting.views.fiscal_year_create import fiscal_year_create

app_name = "accounting"

urlpatterns = [
    # Dashboard
    path("dashboard/", accounting_dashboard, name="dashboard"),

    # Fiscal Years
    path("fiscal-years/", fiscal_year_list, name="fiscal_year_list"),
    path("fiscal-years/new/", fiscal_year_create, name="fiscal_year_create"),  # ← NUEVA RUTA
    path("fiscal-years/<int:fiscal_year_id>/open/", fiscal_year_open, name="fiscal_year_open"),
    path("fiscal-years/<int:fiscal_year_id>/close/", fiscal_year_close, name="fiscal_year_close"),

    # Accounts
    path("accounts/", account_list, name="account_list"),
    path("accounts/new/", account_create, name="account_create"),
    path("accounts/<int:account_id>/edit/", account_edit, name="account_edit"),
    path("accounts/<int:account_id>/delete/", account_delete, name="account_delete"),
    path("accounts/<int:parent_id>/add-child/", account_add_child, name="account_add_child"),

    # Journal
    path("journal/", journal_list, name="journal_list"),
    path("journal/new/", journal_create, name="journal_create"),

    # Periods
    path("periods/", period_list, name="period_list"),
    path("periods/<int:period_id>/open/", period_open, name="period_open"),
    path("periods/<int:period_id>/close/", period_close, name="period_close"),
    path("periods/<int:period_id>/lock/", period_lock, name="period_lock"),

    # Ledger
    path("ledger/<int:account_id>/", ledger_view, name="ledger_view"),

    # Trial Balance
    path("trial-balance/", trial_balance_view, name="trial_balance"),

    # Balance Sheet
    path("balance-sheet/", balance_sheet_view, name="balance_sheet"),
]
