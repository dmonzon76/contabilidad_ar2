from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser
from purchases.forms.purchase import PurchaseLineForm
from purchases.models import Purchase
from suppliers.models import Supplier


class PurchaseCompanyIsolationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="purchase-user",
            password="secret123",
        )
        self.allowed_company = Company.objects.create(
            name="Allowed SRL",
            tax_id="30-55555555-5",
            afip_category="RI",
        )
        other_company = Company.objects.create(
            name="Other SRL",
            tax_id="30-66666666-6",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.allowed_company,
            role="OWNER",
            is_active=True,
        )
        other_supplier = Supplier.objects.create(
            company=other_company,
            name="Other supplier",
        )
        self.other_purchase = Purchase.objects.create(
            company=other_company,
            supplier=other_supplier,
            date=date(2026, 8, 19),
            invoice_number="B-0001",
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.allowed_company.id
        session.save()

    def test_purchase_detail_cannot_access_purchase_from_other_company(self):
        response = self.client.get(
            reverse("purchases:purchase_detail", kwargs={"pk": self.other_purchase.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_purchase_form_only_lists_suppliers_from_active_company(self):
        response = self.client.get(reverse("purchases:purchase_create"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["form"].fields["supplier"].queryset,
            [],
        )

    def test_purchase_line_rejects_negative_unit_price(self):
        form = PurchaseLineForm(
            data={
                "description": "Invalid line",
                "quantity": "1",
                "unit_price": "-10",
                "expense_account": "999999",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("unit_price", form.errors)
