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



class CompanyMiddlewareTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="daniel", password="123")
        self.company = make_company("Test Co")

        # El usuario pertenece a la compañía
        CompanyUser.objects.create(user=self.user, company=self.company, is_default=True)

    def test_returns_active_company(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = {"active_company_id": self.company.id}

        active = get_active_company_from_request(request)
        self.assertEqual(active.pk, self.company.pk)

    def test_raises_error_if_no_active_company(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = {}

        with self.assertRaises(KeyError):
            get_active_company_from_request(request)

    def test_raises_permission_denied_if_user_not_associated(self):
        other_company = make_company("Other Co")

        request = self.factory.get("/")
        request.user = self.user
        request.session = {"active_company_id": other_company.id}

        with self.assertRaises(PermissionDenied):
            get_active_company_from_request(request)

    def test_switch_company_updates_session(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = {"active_company_id": self.company.id}

        new_company = make_company("New Co")
        CompanyUser.objects.create(user=self.user, company=new_company)

        request.session["active_company_id"] = new_company.id

        active = get_active_company_from_request(request)
        self.assertEqual(active.pk, new_company.pk)
