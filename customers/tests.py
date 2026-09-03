from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from company.models import Company, CompanyUser
from customers.models import Customer


class CustomerCompanyIsolationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer-owner",
            password="secret123",
        )
        self.allowed_company = Company.objects.create(
            name="Allowed Customers",
            tax_id="30-33333333-3",
            afip_category="RI",
        )
        self.other_company = Company.objects.create(
            name="Other Customers",
            tax_id="30-44444444-4",
            afip_category="RI",
        )
        CompanyUser.objects.create(
            user=self.user,
            company=self.allowed_company,
            role="OWNER",
            is_active=True,
        )
        self.customer = Customer.objects.create(
            company=self.other_company,
            name="Private Customer",
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["active_company_id"] = self.allowed_company.id
        session.save()

    def test_list_hides_customers_from_other_companies(self):
        response = self.client.get(reverse("customers:customer_list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.customer.name)

    def test_edit_and_delete_reject_customers_from_other_companies(self):
        edit_response = self.client.get(
            reverse("customers:customer_edit", kwargs={"pk": self.customer.pk})
        )
        delete_response = self.client.post(
            reverse("customers:customer_delete", kwargs={"pk": self.customer.pk})
        )

        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(Customer.objects.filter(pk=self.customer.pk).exists())


from django.test import TestCase

# Create your tests here.
