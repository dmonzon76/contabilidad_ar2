from django.test import TestCase
from django.db import IntegrityError

from company.models import Company
from fiscal.models.company_profile import CompanyProfile
from fiscal.forms.company_tax_profile import CompanyTaxProfileForm


class CompanyProfileModelTests(TestCase):

    def test_unique_constraint_prevents_duplicates(self):
        company = Company.objects.create(name="Test Co")
        existing = CompanyProfile.objects.get(company=company)

        with self.assertRaises(IntegrityError):
            CompanyProfile.objects.create(company=company)

    def test_signal_creates_profile_automatically(self):
        company = Company.objects.create(name="Signal Co")

        self.assertTrue(CompanyProfile.objects.filter(company=company).exists())

    def test_get_or_create_always_returns_single_profile(self):
        company = Company.objects.create(name="GetOrCreate Co")

        p1, created1 = CompanyProfile.objects.get_or_create(company=company)
        p2, created2 = CompanyProfile.objects.get_or_create(company=company)

        self.assertEqual(p1.pk, p2.pk)
        self.assertFalse(created2)


class CompanyProfileFormTests(TestCase):

    def test_form_prevents_duplicate_profiles(self):
        company = Company.objects.create(name="Form Co")
        CompanyProfile.objects.get(company=company)

        data = {
            "iibb_status": "LOCAL",
            "ganancias_status": "INSCRIPTO",
            "uses_perceptions": False,
            "uses_retentions": False,
            "vat_21": True,
            "vat_105": False,
            "vat_27": False,
            "vat_exempt": False,
            "vat_non_taxed": False,
        }

        duplicate_instance = CompanyProfile(company=company)
        form = CompanyTaxProfileForm(data=data, instance=duplicate_instance)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "This company already has a tax profile.", form.non_field_errors()
        )
