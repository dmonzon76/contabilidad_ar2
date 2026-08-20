from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser
from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm
from sales.models import Customer, Sale


class SalesCompanyIsolationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="sales-user",
            password="secret123",
        )
        self.allowed_company = Company.objects.create(
            name="Allowed SRL",
            tax_id="30-33333333-3",
            afip_category="RI",
        )
        other_company = Company.objects.create(
            name="Other SRL",
            tax_id="30-44444444-4",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.allowed_company,
            role="OWNER",
            is_active=True,
        )
        other_customer = Customer.objects.create(
            company=other_company,
            name="Other customer",
        )
        self.other_sale = Sale.objects.create(
            company=other_company,
            customer=other_customer,
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.allowed_company.id
        session.save()

    def test_sale_detail_cannot_access_sale_from_other_company(self):
        response = self.client.get(
            reverse("sales:sale_detail", kwargs={"pk": self.other_sale.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_sale_form_only_lists_customers_from_active_company(self):
        response = self.client.get(reverse("sales:sale_create"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["form"].fields["customer"].queryset,
            [],
        )

    def test_sale_number_is_generated_and_not_user_editable(self):
        customer = Customer.objects.create(
            company=self.allowed_company,
            name="Allowed customer",
        )
        form = SaleForm(
            data={"customer": customer.id},
            company_id=self.allowed_company.id,
        )

        self.assertTrue(form.is_valid())
        self.assertNotIn("number", form.fields)
        sale = form.save(commit=False)
        sale.company = self.allowed_company
        sale.save()
        self.assertEqual(sale.number, "000001")

    def test_sale_item_rejects_non_positive_quantity(self):
        form = SaleItemForm(
            data={
                "description": "Invalid item",
                "quantity": "0",
                "unit_price": "10",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
