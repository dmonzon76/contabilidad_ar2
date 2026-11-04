from django.views.generic import DetailView

from payroll.models import Employee


class EmployeeDeactivateConfirmView(
    DetailView,
):

    model = Employee

    template_name = (
        "payroll/employees/employee_deactivate.html"
    )

    context_object_name = "employee"