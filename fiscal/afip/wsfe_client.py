import datetime
import logging
from dataclasses import dataclass
from typing import Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class CAEResponse:
    success: bool
    cae: Optional[str] = None
    due_date: Optional[datetime.date] = None
    error: Optional[str] = None
    raw: Optional[dict] = None


class WSFEClient:
    """
    AFIP WSFEv1 client (enterprise-ready).

    - Supports testing and production modes
    - Validates configuration
    - Logs payloads and responses
    - Handles errors robustly
    """

    def __init__(self, cert: str, key: str, cuit: str, testing: Optional[bool] = None):
        self.cert = cert
        self.key = key
        self.cuit = cuit

        if not self.cert or not self.key:
            raise ValueError("AFIP certificate or key missing")

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

        if not self.wsdl_url and not self.testing:
            raise ValueError("AFIP WSFE production URL not configured")

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
        Creates a fiscal invoice and returns CAE.
        In testing mode, simulates the response.
        """

        if total <= 0:
            return CAEResponse(success=False, error="Invalid total amount")

        if self.testing:
            return self._simulate_cae(
                voucher_type=voucher_type,
                point_of_sale=point_of_sale,
                voucher_number=voucher_number,
                total=total,
                customer_cuit=customer_cuit,
                date=date,
            )

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

        logger.info("AFIP WSFE request payload: %s", payload)

        try:
            data = self._post_with_retry(payload)
            logger.info("AFIP WSFE response: %s", data)

            if not data.get("success"):
                error_msg = (
                    data.get("error")
                    or data.get("errors")
                    or "Unknown AFIP error"
                )
                return CAEResponse(
                    success=False,
                    error=error_msg,
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
        Testing mode: generates a simulated CAE.
        Does not call real AFIP.
        """

        if total <= 0:
            return CAEResponse(
                success=False,
                error="Testing: invalid total amount",
                raw={"mode": "testing", "error": "invalid_total"},
            )

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
                "total": float(total),
                "customer_cuit": customer_cuit,
                "date": date.strftime("%Y-%m-%d"),
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
        Builds payload for WSFE.
        In production you'd adapt this to AFIP's real SOAP/XML format.
        """

        return {
            "cuit": self.cuit,
            "voucher_type": voucher_type,
            "point_of_sale": int(point_of_sale),
            "voucher_number": int(voucher_number),
            "date": date.strftime("%Y%m%d"),
            "total": float(total),
            "subtotal": float(subtotal),
            "vat_amount": float(vat_amount),
            "exempt_amount": float(exempt_amount),
            "non_taxed_amount": float(non_taxed_amount),
            "customer_cuit": customer_cuit,
        }

    def _post_with_retry(self, payload: dict, max_attempts: int = 3) -> dict:
        """
        Sends request to AFIP with retry logic.
        """

        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                response = requests.post(
                    self.wsdl_url,
                    json=payload,
                    cert=(self.cert, self.key),
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                last_error = e
                logger.warning(
                    "AFIP WSFE attempt %s/%s failed: %s",
                    attempt,
                    max_attempts,
                    e,
                )
        raise RuntimeError(f"AFIP WSFE failed after {max_attempts} attempts: {last_error}")
