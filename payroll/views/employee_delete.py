from django.urls import reverse_lazy
from django.views.generic import DeleteView

from payroll.models import Employee


class EmployeeDeleteView(DeleteView):

    model = Employee

    template_name = (
        "payroll/employees/employee_confirm_delete.html"
    )

    success_url = reverse_lazy(
        "payroll:employee_list"
    )

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.active_company,
        )