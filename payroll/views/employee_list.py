from django.views.generic import ListView

from payroll.models import Employee


class EmployeeListView(ListView):

    model = Employee

    template_name = (
        "payroll/employees/employee_list.html"
    )

    context_object_name = (
        "employees"
    )

    paginate_by = 25

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.active_company,
        ).order_by(
            "last_name",
            "first_name",
        )