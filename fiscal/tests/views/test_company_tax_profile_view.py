from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from company.models import Company, UserCompany
from fiscal.models.company_profile import CompanyProfile


def make_company(name):
    return Company.objects.create(
        name=name,
        tax_id="30000000001",
        afip_category="RI",
    )


class CompanyTaxProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="daniel", password="123")
        self.company_a = make_company("Company A")
        self.company_b = make_company("Company B")

        UserCompany.objects.create(
            user=self.user,
            company=self.company_a,
            is_active=True,
            is_default=True,
        )

        self.profile_a = CompanyProfile.objects.get(company=self.company_a)

    def test_requires_login(self):
        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 302)

    def test_requires_active_company(self):
        self.client.login(username="daniel", password="123")
        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 400)

    def test_denies_access_to_other_company(self):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_b.id
        session.save()

        with self.assertRaises(PermissionDenied):
            self.client.get(reverse("fiscal:company_tax_profile"))

    def test_loads_profile_correctly(self):
        self.client.login(username="daniel", password="123")

        session = self.client.session
        session["active_company_id"] = self.company_a.id
        session.save()

        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company_a.name)
