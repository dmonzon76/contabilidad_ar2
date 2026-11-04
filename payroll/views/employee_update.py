from django.urls import reverse_lazy
from django.views.generic import UpdateView

from payroll.models import Employee


class EmployeeUpdateView(UpdateView):

    model = Employee

    template_name = (
        "payroll/employees/employee_form.html"
    )

    fields = [
        "first_name",
        "last_name",
        "employee_number",
        "cuil",
        "hire_date",
        "is_active",
    ]

    success_url = reverse_lazy(
        "payroll:employee_list"
    )