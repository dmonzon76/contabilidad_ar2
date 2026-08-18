from django.urls import path

# --- EXISTING VIEWS ---
from fiscal.views.afip_activity import (
    afip_activity_list,
    afip_activity_create,
    afip_activity_edit,
)

from fiscal.views.company_tax import company_tax_profile

from fiscal.views.thirdparty_tax import (
    thirdparty_tax_list,
    thirdparty_tax_edit,
)

from fiscal.views.electronic_voucher_book import (
    electronic_voucher_book_list,
    electronic_voucher_book_create,
    electronic_voucher_book_edit,
    electronic_voucher_book_delete,
)

# --- NEW FISCAL MODULE VIEWS ---
from fiscal.views.fiscal_invoice import (
    fiscal_invoice_list,
    fiscal_invoice_detail,
    fiscal_invoice_create,
)

from fiscal.views.fiscal_product import (
    fiscal_product_list,
    fiscal_product_create,
    fiscal_product_edit,
)

from fiscal.views.fiscal_service import (
    fiscal_service_list,
    fiscal_service_create,
    fiscal_service_edit,
)

app_name = "fiscal"

urlpatterns = [

    # -------------------------
    # AFIP ACTIVITIES
    # -------------------------
    path("afip/", afip_activity_list, name="afip_activity_list"),
    path("afip/new/", afip_activity_create, name="afip_activity_create"),
    path("afip/<int:pk>/edit/", afip_activity_edit, name="afip_activity_edit"),

    # -------------------------
    # COMPANY TAX PROFILE
    # -------------------------
    path("company/", company_tax_profile, name="company_tax_profile"),

    # -------------------------
    # THIRD PARTY TAX PROFILES
    # -------------------------
    path("thirdparty/", thirdparty_tax_list, name="thirdparty_tax_list"),
    path("thirdparty/<int:pk>/edit/", thirdparty_tax_edit, name="thirdparty_tax_edit"),

    # -------------------------
    # ELECTRONIC VOUCHER BOOKS
    # -------------------------
    path("electronic-voucher-books/", electronic_voucher_book_list, name="electronic_voucher_book_list"),
    path("electronic-voucher-books/new/", electronic_voucher_book_create, name="electronic_voucher_book_create"),
    path("electronic-voucher-books/<int:book_id>/edit/", electronic_voucher_book_edit, name="electronic_voucher_book_edit"),
    path("electronic-voucher-books/<int:book_id>/delete/", electronic_voucher_book_delete, name="electronic_voucher_book_delete"),

    # -------------------------
    # FISCAL INVOICES (nuevo flujo)
    # -------------------------
    path("invoices/", fiscal_invoice_list, name="fiscal_invoice_list"),
    path("invoices/<int:pk>/", fiscal_invoice_detail, name="fiscal_invoice_detail"),
    path("invoices/create/<int:sale_id>/", fiscal_invoice_create, name="fiscal_invoice_create"),

    # -------------------------
    # FISCAL PRODUCTS
    # -------------------------
    path("products/", fiscal_product_list, name="fiscal_product_list"),
    path("products/new/", fiscal_product_create, name="fiscal_product_create"),
    path("products/<int:pk>/edit/", fiscal_product_edit, name="fiscal_product_edit"),

    # -------------------------
    # FISCAL SERVICES
    # -------------------------
    path("services/", fiscal_service_list, name="fiscal_service_list"),
    path("services/new/", fiscal_service_create, name="fiscal_service_create"),
    path("services/<int:pk>/edit/", fiscal_service_edit, name="fiscal_service_edit"),
]
