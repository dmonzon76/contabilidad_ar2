from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from company.models import Company, CompanyUser
from payroll.models import Employee


class EmployeeCompanyIsolationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="payroll-user",
            password="secret123",
        )
        self.company = Company.objects.create(
            name="Company One",
            tax_id="30-11111111-1",
            afip_category="RI",
        )
        self.other_company = Company.objects.create(
            name="Company Two",
            tax_id="30-22222222-2",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.company,
            role="OWNER",
            is_active=True,
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.company.id
        session.save()

    def create_employee(self, company, employee_number):
        return Employee.objects.create(
            company=company,
            employee_number=employee_number,
            first_name="Ana",
            last_name="Perez",
            cuil="20123456789",
            hire_date="2024-01-01",
        )

    def test_employee_list_only_shows_active_company_employees(self):
        own_employee = self.create_employee(self.company, "EMP-1")
        self.create_employee(self.other_company, "EMP-2")

        response = self.client.get(reverse("payroll:employee_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["employees"]), [own_employee])

    def test_new_employee_is_assigned_to_active_company(self):
        response = self.client.post(
            reverse("payroll:employee_create"),
            {
                "employee_number": "EMP-NEW",
                "first_name": "Ana",
                "last_name": "Perez",
                "cuil": "20123456789",
                "nationality": "Argentina",
                "hire_date": "2024-01-01",
            },
        )

        self.assertRedirects(response, reverse("payroll:employee_list"))
        employee = Employee.objects.get(employee_number="EMP-NEW")
        self.assertEqual(employee.company, self.company)

    def test_other_company_employee_is_not_accessible_by_id(self):
        employee = self.create_employee(self.other_company, "EMP-OTHER")

        urls_and_methods = (
            (reverse("payroll:employee_detail", kwargs={"pk": employee.pk}), "get"),
            (reverse("payroll:employee_update", kwargs={"pk": employee.pk}), "get"),
            (reverse("payroll:employee_delete", kwargs={"pk": employee.pk}), "get"),
            (
                reverse("payroll:employee_deactivate_confirm", kwargs={"pk": employee.pk}),
                "get",
            ),
            (reverse("payroll:employee_deactivate", kwargs={"pk": employee.pk}), "post"),
        )
        for url, method in urls_and_methods:
            with self.subTest(url=url, method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 404)
