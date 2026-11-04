from django.views.generic import DetailView

from payroll.models import (
    Employee,
    EmployeePosition,
    PayrollReceipt,
)


class EmployeeDetailView(DetailView):

    model = Employee

    template_name = (
        "payroll/employees/employee_detail.html"
    )

    context_object_name = "employee"

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        employee = self.object

        current_position = (
            EmployeePosition.objects
            .filter(
                employee=employee,
                is_active=True,
            )
            .select_related(
                "category",
            )
            .first()
        )

        last_receipt = (
            PayrollReceipt.objects
            .filter(
                employee=employee,
            )
            .order_by(
                "-period__year",
                "-period__month",
            )
            .first()
        )

        context[
            "current_position"
        ] = current_position

        context[
            "last_receipt"
        ] = last_receipt

        return context