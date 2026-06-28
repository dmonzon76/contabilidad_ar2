from django.urls import path

from accounting.views.account import (
    account_list,
    account_create,
    account_edit,
    account_delete,
    account_add_child,   # ← NUEVO
    period_list,
    period_open,
    period_close,
    period_lock,
)

from accounting.views.journal import (
    journal_list,
    journal_create,
)
app_name = "accounting"

urlpatterns = [
    # Accounts
    path("accounts/", account_list, name="account_list"),
    path("accounts/new/", account_create, name="account_create"),
    path("accounts/<int:account_id>/edit/", account_edit, name="account_edit"),
    path("accounts/<int:account_id>/delete/", account_delete, name="account_delete"),

    # NEW: Add child account
    path("accounts/<int:parent_id>/add-child/", account_add_child, name="account_add_child"),

    # Journal
    path("journal/", journal_list, name="journal_list"),
    path("journal/new/", journal_create, name="journal_create"),

    # Periods
    path("periods/", period_list, name="period_list"),
    path("periods/<int:period_id>/open/", period_open, name="period_open"),
    path("periods/<int:period_id>/close/", period_close, name="period_close"),
    path("periods/<int:period_id>/lock/", period_lock, name="period_lock"),
]

from accounting.views.ledger import ledger_view

path("ledger/<int:account_id>/", ledger_view, name="ledger_view"),

from accounting.views.trial_balance import trial_balance_view

path("trial-balance/", trial_balance_view, name="trial_balance"),

from accounting.views.balance_sheet import balance_sheet_view

path("balance-sheet/", balance_sheet_view, name="balance_sheet"),


