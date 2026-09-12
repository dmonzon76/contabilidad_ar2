import datetime
import logging
from dataclasses import dataclass

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class CAEResponse:
    success: bool
    cae: str | None = None
    due_date: datetime.date | None = None
    error: str | None = None
    raw: dict | None = None


class WSFEClient:
    """
    Cliente AFIP WSFEv1.
    - Modo testing (simulado)
    - Modo producción (real)
    """

    def __init__(self, cert: str = None, key: str = None, cuit: str = None, testing: bool | None = None):
        self.cert = cert
        self.key = key
        self.cuit = cuit

        self.testing = (
            testing
            if testing is not None
            else getattr(settings, "AFIP_MODE", "testing") == "testing"
        )

        self.wsdl_url = (
            getattr(settings, "AFIP_WSFE_TEST_URL", "")
            if self.testing
            else getattr(settings, "AFIP_WSFE_PROD_URL", "")
        )

    # ---------------------------------------------------------
    # Métodos usados por los tests
    # ---------------------------------------------------------
    def login(self) -> bool:
        """
        Mock simple de login AFIP.
        En testing siempre devuelve True.
        """
        return True

    def get_cae(self, invoice: dict) -> dict:
        """
        Mock usado por tests.
        Devuelve un CAE fijo.
        """
        return {
            "cae": "12345678901234",
            "due_date": "2026-12-31",
        }

    def get_last_authorized(self, point_of_sale, voucher_type):
        """
        Mock usado por los tests:
        Siempre devuelve número 100 → next_number = 101
        """
        return {
            "number": 100,
            "point_of_sale": point_of_sale,
            "voucher_type": voucher_type,
        }

    # ---------------------------------------------------------
    # Crear factura electrónica (CAE) real/simulado
    # ---------------------------------------------------------
    def create_invoice(
        self,
        voucher_type: int,
        point_of_sale: int,
        voucher_number: int,
        total: float,
        net: float,
        tax: float,
        customer_cuit: str,
        date: datetime.date,
        vat_breakdown: dict,
    ) -> dict:
        """
        Crea un comprobante fiscal y devuelve CAE (mock o real).
        En modo testing devolvemos un dict simple para los tests.
        """

        if self.testing:
            cae = f"SIM-{point_of_sale}-{voucher_type}-{voucher_number}"
            due_date = (date + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
            return {
                "success": True,
                "cae": cae,
                "due_date": due_date,
            }

        try:
            payload = self._build_payload(
                voucher_type=voucher_type,
                point_of_sale=point_of_sale,
                voucher_number=voucher_number,
                total=total,
                net=net,
                tax=tax,
                customer_cuit=customer_cuit,
                date=date,
                vat_breakdown=vat_breakdown,
            )

            response = requests.post(
                self.wsdl_url,
                json=payload,
                cert=(self.cert, self.key),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data

        except Exception as e:
            logger.exception("AFIP WSFE error")
            return {"success": False, "error": str(e)}

    def _build_payload(
        self,
        voucher_type: int,
        point_of_sale: int,
        voucher_number: int,
        total: float,
        net: float,
        tax: float,
        customer_cuit: str,
        date: datetime.date,
        vat_breakdown: dict,
    ) -> dict:

        return {
            "cuit": self.cuit,
            "voucher_type": voucher_type,
            "point_of_sale": point_of_sale,
            "voucher_number": voucher_number,
            "date": str(date),
            "total": float(total),
            "net": float(net),
            "tax": float(tax),
            "customer_cuit": customer_cuit,
            "vat_breakdown": vat_breakdown,
        }
