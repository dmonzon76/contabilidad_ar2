from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import View

from payroll.models import Employee


class EmployeeDeactivateView(View):

    def post(
        self,
        request,
        pk,
    ):

        employee = get_object_or_404(
            Employee,
            pk=pk,
            company=request.active_company,
        )

        employee.is_active = False

        employee.save()

        return redirect(
            "payroll:employee_list"
        )