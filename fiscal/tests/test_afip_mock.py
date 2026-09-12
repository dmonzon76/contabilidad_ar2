from django.test import TestCase
from unittest.mock import patch

from fiscal.afip.wsfe_client import WSFEClient


class AFIPMockTests(TestCase):

    @patch.object(WSFEClient, "login", return_value=True)
    @patch.object(
        WSFEClient,
        "get_cae",
        return_value={"cae": "123456", "due_date": "2026-12-31"}
    )
    def test_get_cae_mock(self, mock_get_cae, mock_login):
        client = WSFEClient()
        self.assertTrue(client.login())

        result = client.get_cae({})
        self.assertEqual(result["cae"], "123456")
        self.assertEqual(result["due_date"], "2026-12-31")

    @patch.object(
        WSFEClient,
        "get_last_authorized",
        return_value={"number": 150, "point_of_sale": 1, "voucher_type": "A"}
    )
    def test_get_last_authorized_mock(self, mock_last):
        client = WSFEClient()
        result = client.get_last_authorized(1, "A")

        self.assertEqual(result["number"], 150)
        self.assertEqual(result["point_of_sale"], 1)
        self.assertEqual(result["voucher_type"], "A")

    @patch.object(
        WSFEClient,
        "create_invoice",
        return_value={"success": True, "cae": "99999999", "due_date": "2027-01-01"}
    )
    def test_create_invoice_mock(self, mock_create):
        client = WSFEClient()
        result = client.create_invoice(
            voucher_type=1,
            point_of_sale=1,
            voucher_number=1,
            total=100,
            net=100,
            tax=0,
            customer_cuit="20123456789",
            date="2026-01-01",
            vat_breakdown={},
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["cae"], "99999999")
        self.assertEqual(result["due_date"], "2027-01-01")

    @patch.object(
        WSFEClient,
        "get_cae",
        side_effect=Exception("AFIP error: rejected")
    )
    def test_afip_error_mock(self, mock_get_cae):
        client = WSFEClient()

        with self.assertRaises(Exception):
            client.get_cae({})
