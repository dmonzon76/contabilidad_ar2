from .AFIPactivities import AFIPActivity
from .company_profile import CompanyProfile
from .electronic_voucher_book import ElectronicVoucherBook
from .fiscal_invoice import FiscalInvoice
from .fiscal_invoice_line import FiscalInvoiceLine
from .fiscal_product import FiscalProduct
from .fiscal_service import FiscalService
from .jurisdiction_coefficient import JurisdictionCoefficient
from .tax import Tax
from .tax_regime import TaxRegime
from .thirdparty_tax import ThirdPartyTaxProfile
from .thirdparty_tax_rule import ThirdPartyTaxRule

__all__ = [
    "AFIPActivity",
    "ThirdPartyTaxProfile",
    "CompanyProfile",
    "ElectronicVoucherBook",
    "FiscalInvoice",
    "FiscalInvoiceLine",
    "FiscalProduct",
    "FiscalService",
    "Tax",
    "TaxRegime",
    "ThirdPartyTaxRule",
    "JurisdictionCoefficient",
]


