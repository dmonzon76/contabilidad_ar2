from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser
from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from suppliers.forms.supplier import SupplierForm
from suppliers.models import Supplier


class SupplierCompanyTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="supplier-user",
            password="test-password",
        )
        self.company = Company.objects.create(
            name="Active Company",
            tax_id="30-11111111-1",
            afip_category="RI",
        )
        self.other_company = Company.objects.create(
            name="Other Company",
            tax_id="30-22222222-2",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.company,
            role="OWNER",
            is_active=True,
        )
        self.profile = ThirdPartyTaxProfile.objects.create(
            company=self.company,
            name="Active profile",
        )
        self.other_profile = ThirdPartyTaxProfile.objects.create(
            company=self.other_company,
            name="Other profile",
        )

        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.company.pk
        session.save()

    def test_add_view_loads_form_for_active_company(self):
        response = self.client.get(reverse("suppliers:supplier_add"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["form"].fields["tax_profile"].queryset),
            [self.profile],
        )

    def test_edit_view_loads_form_for_active_company(self):
        supplier = Supplier.objects.create(
            company=self.company,
            name="Existing supplier",
            tax_id="30-88888888-8",
            tax_profile=self.profile,
        )

        response = self.client.get(reverse("suppliers:supplier_edit", args=[supplier.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["form"].fields["tax_profile"].queryset),
            [self.profile],
        )

    def test_form_rejects_tax_profile_from_another_company(self):
        form = SupplierForm(
            {
                "name": "New supplier",
                "tax_profile": self.other_profile.pk,
            },
            company=self.company,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("tax_profile", form.errors)

    def test_tax_id_is_required(self):
        form = SupplierForm({"name": "New supplier"}, company=self.company)

        self.assertFalse(form.is_valid())
        self.assertIn("tax_id", form.errors)
