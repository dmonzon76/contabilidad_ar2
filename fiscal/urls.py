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
from fiscal.views import (
    fiscal_invoice_list,
    fiscal_invoice_create,
    fiscal_invoice_edit,
    fiscal_invoice_line_create,

    fiscal_product_list,
    fiscal_product_create,
    fiscal_product_edit,

    fiscal_service_list,
    fiscal_service_create,
    fiscal_service_edit,

    fiscal_sale_list,
    fiscal_sale_create,
    fiscal_sale_generate_invoice,
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
    # FISCAL INVOICES
    # -------------------------
    path("invoices/", fiscal_invoice_list, name="fiscal_invoice_list"),
    path("invoices/new/", fiscal_invoice_create, name="fiscal_invoice_create"),
    path("invoices/<int:pk>/edit/", fiscal_invoice_edit, name="fiscal_invoice_edit"),

    # Invoice Lines
    path("invoices/<int:invoice_id>/lines/new/", fiscal_invoice_line_create, name="fiscal_invoice_line_create"),

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

    # -------------------------
    # FISCAL SALES
    # -------------------------
    path("sales/", fiscal_sale_list, name="fiscal_sale_list"),
    path("sales/new/", fiscal_sale_create, name="fiscal_sale_create"),
    path("sales/<int:pk>/generate-invoice/", fiscal_sale_generate_invoice, name="fiscal_sale_generate_invoice"),
]
