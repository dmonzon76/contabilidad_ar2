from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser


class DashboardActiveCompanyTests(TestCase):
    def test_dashboard_uses_session_active_company(self):
        user = get_user_model().objects.create_user(
            username="alice",
            password="secret123",
        )
        company = Company.objects.create(
            name="Acme SRL",
            tax_id="30-12345678-9",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=user,
            company=company,
            role="OWNER",
            is_active=True,
        )

        self.client.force_login(user)
        session = self.client.session
        session["active_company_id"] = company.id
        session.save()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["company"].id, company.id)
