from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyProfile, CompanyUser


class CompanyCreateTests(TestCase):
    def test_creator_is_owner_of_new_company(self):
        user = get_user_model().objects.create_user(
            username="owner",
            password="secret123",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("company:company_create"),
            {
                "name": "Acme SRL",
                "tax_id": "30-12345678-9",
                "afip_category": "RI",
                "address": "Main Street 1",
                "city": "Buenos Aires",
                "province": "Buenos Aires",
            },
        )

        company = Company.objects.get(tax_id="30-12345678-9")
        self.assertRedirects(response, reverse("company:company_list"))
        self.assertTrue(CompanyProfile.objects.filter(company=company).exists())
        self.assertTrue(
            CompanyUser.objects.filter(
                user=user,
                company=company,
                role="OWNER",
                is_active=True,
            ).exists()
        )


class CompanyAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="member",
            password="secret123",
        )
        self.allowed_company = Company.objects.create(
            name="Allowed SRL",
            tax_id="30-11111111-1",
            afip_category="RI",
        )
        self.other_company = Company.objects.create(
            name="Other SRL",
            tax_id="30-22222222-2",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.allowed_company,
            role="OWNER",
            is_active=True,
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.allowed_company.id
        session.save()

    def test_company_list_only_shows_companies_user_can_access(self):
        response = self.client.get(reverse("company:company_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["companies"]), [self.allowed_company])

    def test_company_edit_rejects_company_user_cannot_access(self):
        response = self.client.get(
            reverse(
                "company:company_edit",
                kwargs={"company_id": self.other_company.id},
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_selecting_company_requires_post(self):
        response = self.client.get(
            reverse(
                "company:company_set_active",
                kwargs={"company_id": self.other_company.id},
            )
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            self.client.session.get("active_company_id"),
            self.allowed_company.id,
        )

    def test_user_can_select_another_company_they_belong_to(self):
        CompanyUser.objects.create(
            user=self.user,
            company=self.other_company,
            role="VIEWER",
            is_active=True,
        )

        response = self.client.post(
            reverse(
                "company:company_set_active",
                kwargs={"company_id": self.other_company.id},
            )
        )

        self.assertRedirects(response, reverse("main_dashboard"))
        self.assertEqual(
            self.client.session.get("active_company_id"),
            self.other_company.id,
        )

    def test_accounting_is_blocked_without_view_permission(self):
        CompanyUser.objects.filter(
            user=self.user,
            company=self.allowed_company,
        ).update(can_view_accounting=False)

        response = self.client.get(reverse("accounting:account_list"))

        self.assertEqual(response.status_code, 403)
