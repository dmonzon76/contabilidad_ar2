from django.urls import path

from payroll.views.dashboard import PayrollDashboardView
from payroll.views.employee_create import EmployeeCreateView
from payroll.views.employee_deactivate import EmployeeDeactivateView
from payroll.views.employee_deactivate_confirm import EmployeeDeactivateConfirmView
from payroll.views.employee_delete import EmployeeDeleteView
from payroll.views.employee_detail import EmployeeDetailView
from payroll.views.employee_list import EmployeeListView
from payroll.views.employee_update import EmployeeUpdateView
from payroll.views.family_member_create import FamilyMemberCreateView
from payroll.views.family_member_update import FamilyMemberUpdateView
from payroll.views.payroll_receipt_detail import PayrollReceiptDetailView

urlpatterns = [
    path(
        "dashboard/",
        PayrollDashboardView.as_view(),
        name="dashboard",
),

    path(
        "receipts/<int:pk>/",
        PayrollReceiptDetailView.as_view(),
        name="payroll_receipt_detail",
    ),
    path(
    "employees/",
    EmployeeListView.as_view(),
    name="employee_list",
),
path(
    "employees/<int:pk>/",
    EmployeeDetailView.as_view(),
    name="employee_detail",
),
path(
    "employees/<int:pk>/edit/",
    EmployeeUpdateView.as_view(),
    name="employee_update",
),
path(
    "employees/create/",
    EmployeeCreateView.as_view(),
    name="employee_create",
),
path(
    "employees/<int:pk>/delete/",
    EmployeeDeleteView.as_view(),
    name="employee_delete",
),
path(
    "employees/<int:pk>/deactivate/",
    EmployeeDeactivateView.as_view(),
    name="employee_deactivate",
),
path(
    "employees/<int:pk>/deactivate/confirm/",
    EmployeeDeactivateConfirmView.as_view(),
    name="employee_deactivate_confirm",
),

path(
    "employees/<int:pk>/deactivate/confirm/",
    EmployeeDeactivateView.as_view(),
    name="employee_deactivate_confirm",
),
path(
    "employees/<int:employee_id>/family/new/",
    FamilyMemberCreateView.as_view(),
    name="family_member_create",
),
path(
    "family/<int:pk>/edit/",
    FamilyMemberUpdateView.as_view(),
    name="family_member_update",
),
path(
        "dashboard/",
        PayrollDashboardView.as_view(),
        name="dashboard",
    ),

]
