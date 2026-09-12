from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from company.models import Company, CompanyUser
from fiscal.models.company_profile import CompanyProfile


class CompanyTaxViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="daniel", password="123")
        self.company = Company.objects.create(
            name="Test Co",
            tax_id="30000000001",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.company,
            role="OWNER",
            is_active=True,
        )
        self.profile = CompanyProfile.objects.get(company=self.company)

    def test_requires_login(self):
        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 302)

    def test_requires_active_company(self):
        self.client.login(username="daniel", password="123")
        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 302)

    def test_loads_profile_correctly(self):
        self.client.login(username="daniel", password="123")
        session = self.client.session
        session["active_company_id"] = self.company.id
        session.save()

        response = self.client.get(reverse("fiscal:company_tax_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company.name)
