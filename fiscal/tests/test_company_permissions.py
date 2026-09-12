from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from company.models import Company, CompanyUser

from fiscal.middleware.company_middleware import get_active_company_from_request

import uuid

def make_company(name):
    return Company.objects.create(
        name=name,
        tax_id=str(uuid.uuid4())[:11],  # CUIT único
        afip_category="RI",
    )


class CompanyPermissionTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username="daniel", password="123")
        self.company_a = make_company("Company A")
        self.company_b = make_company("Company B")

        # El usuario pertenece solo a Company A
        CompanyUser.objects.create(
            user=self.user,
            company=self.company_a,
            is_active=True,
            is_default=True,
        )

    def test_user_can_access_own_company(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = {"active_company_id": self.company_a.id}

        company = get_active_company_from_request(request)
        self.assertEqual(company.pk, self.company_a.pk)

    def test_user_cannot_access_other_company(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = {"active_company_id": self.company_b.id}

        with self.assertRaises(PermissionDenied):
            get_active_company_from_request(request)

    def test_user_without_company_association_is_denied(self):
        user2 = User.objects.create_user(username="other", password="123")

        request = self.factory.get("/")
        request.user = user2
        request.session = {"active_company_id": self.company_a.id}

        with self.assertRaises(PermissionDenied):
            get_active_company_from_request(request)
