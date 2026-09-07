from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser
from accounting.models import Account
from fiscal.models.tax import Tax
from purchases.forms.purchase import PurchaseLineForm
from purchases.models import (
    Purchase,
    PurchaseLine,
    PurchasePerception,
    PurchaseRetention,
    PurchaseTax,
)
from suppliers.models import Supplier, ThirdPartyTaxProfile


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
        self.assertIn("line_formset", response.context)
        self.assertIn("tax_formset", response.context)
        self.assertIn("perception_formset", response.context)
        self.assertIn("retention_formset", response.context)
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

    def test_purchase_calculates_tax_perception_retention_and_total(self):
        profile = ThirdPartyTaxProfile.objects.create(
            company=self.allowed_company,
            name="RI supplier profile",
            iva_condition="RI",
            iibb_rate="1.00",
            ganancias_rate="0.00",
        )
        supplier = Supplier.objects.create(
            company=self.allowed_company,
            name="Fiscal supplier",
            tax_profile=profile,
        )
        account = Account.objects.create(
            company=self.allowed_company,
            code="6.1.01",
            name="Services",
            account_type="EXPENSE",
        )
        tax = Tax.objects.create(
            code="TEST_IVA_21",
            name="Test IVA 21%",
            rate="21.00",
            is_vat=True,
        )
        purchase = Purchase.objects.create(
            company=self.allowed_company,
            supplier=supplier,
            date=date(2026, 9, 4),
            invoice_number="A-0001",
        )
        PurchaseLine.objects.create(
            purchase=purchase,
            description="Service",
            quantity="1.00",
            unit_price="100.00",
            expense_account=account,
        )
        PurchaseTax.objects.create(purchase=purchase, tax=tax, base_amount="100.00")
        PurchasePerception.objects.create(purchase=purchase, perception_type="IIBB")
        PurchaseRetention.objects.create(purchase=purchase, retention_type="IVA")

        purchase.calculate_totals()
        purchase.refresh_from_db()

        self.assertEqual(purchase.net_amount, 100)
        self.assertEqual(purchase.tax_amount, 21)
        self.assertEqual(purchase.perception_amount, 1)
        self.assertEqual(purchase.retention_amount, 10.5)
        self.assertEqual(purchase.total_amount, 111.5)
