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
    Soporta:
    - modo testing (simulado)
    - modo producción (real)
    """

    def __init__(self, cert: str, key: str, cuit: str, testing: bool | None = None):
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

    def create_invoice(
        self,
        voucher_type: str,
        point_of_sale: int,
        voucher_number: int,
        total: float,
        subtotal: float,
        vat_amount: float,
        exempt_amount: float,
        non_taxed_amount: float,
        customer_cuit: str,
        date: datetime.date,
    ) -> CAEResponse:
        """
        Crea un comprobante fiscal y devuelve CAE.
        En modo testing, simula la respuesta.
        """

        if self.testing:
            return self._simulate_cae(
                voucher_type=voucher_type,
                point_of_sale=point_of_sale,
                voucher_number=voucher_number,
                total=total,
                customer_cuit=customer_cuit,
                date=date,
            )

        try:
            payload = self._build_payload(
                voucher_type=voucher_type,
                point_of_sale=point_of_sale,
                voucher_number=voucher_number,
                total=total,
                subtotal=subtotal,
                vat_amount=vat_amount,
                exempt_amount=exempt_amount,
                non_taxed_amount=non_taxed_amount,
                customer_cuit=customer_cuit,
                date=date,
            )

            # Ejemplo simplificado: en la práctica usarías SOAP o requests con XML
            response = requests.post(
                self.wsdl_url,
                json=payload,
                cert=(self.cert, self.key),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                return CAEResponse(
                    success=False,
                    error=data.get("error", "Unknown AFIP error"),
                    raw=data,
                )

            cae = data["cae"]
            due_date_str = data["due_date"]
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()

            return CAEResponse(
                success=True,
                cae=cae,
                due_date=due_date,
                raw=data,
            )

        except Exception as e:
            logger.exception("AFIP WSFE error")
            return CAEResponse(success=False, error=str(e))

    def _simulate_cae(
        self,
        voucher_type: str,
        point_of_sale: int,
        voucher_number: int,
        total: float,
        customer_cuit: str,
        date: datetime.date,
    ) -> CAEResponse:
        """
        Modo testing: genera un CAE simulado.
        No llama a AFIP real.
        """

        cae = f"SIM-{point_of_sale}-{voucher_type}-{voucher_number}"
        due_date = date + datetime.timedelta(days=10)

        return CAEResponse(
            success=True,
            cae=cae,
            due_date=due_date,
            raw={
                "mode": "testing",
                "voucher_type": voucher_type,
                "point_of_sale": point_of_sale,
                "voucher_number": voucher_number,
                "total": total,
                "customer_cuit": customer_cuit,
                "date": str(date),
            },
        )

    def _build_payload(
        self,
        voucher_type: str,
        point_of_sale: int,
        voucher_number: int,
        total: float,
        subtotal: float,
        vat_amount: float,
        exempt_amount: float,
        non_taxed_amount: float,
        customer_cuit: str,
        date: datetime.date,
    ) -> dict:
        """
        Arma el payload para WSFE.
        En producción lo adaptarías al formato real (SOAP/XML).
        """

        return {
            "cuit": self.cuit,
            "voucher_type": voucher_type,
            "point_of_sale": point_of_sale,
            "voucher_number": voucher_number,
            "date": str(date),
            "total": float(total),
            "subtotal": float(subtotal),
            "vat_amount": float(vat_amount),
            "exempt_amount": float(exempt_amount),
            "non_taxed_amount": float(non_taxed_amount),
            "customer_cuit": customer_cuit,
        }
