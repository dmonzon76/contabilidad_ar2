from django.urls import reverse_lazy
from django.views.generic import UpdateView

from payroll.models import Employee


class EmployeeUpdateView(UpdateView):

    model = Employee

    template_name = (
        "payroll/employees/employee_form.html"
    )

    fields = [

    # Identificación

    "employee_number",
    "first_name",
    "last_name",

    "dni",
    "cuil",

    # Personales

    "birth_date",
    "nationality",
    "gender",
    "marital_status",

    # Domicilio

    "street",
    "street_number",
    "city",
    "province",
    "postal_code",

    # Contacto

    "email",
    "mobile_phone",

    # Emergencias

    "emergency_contact_name",
    "emergency_contact_phone",

    # Bancarios

    "bank_name",
    "cbu",

    # Laboral

    "hire_date",
    "is_active",
]

    success_url = reverse_lazy(
        "payroll:employee_list"
    )

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.active_company,
        )