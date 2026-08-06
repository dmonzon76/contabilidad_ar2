from django.contrib import admin
from django.urls import include, path
from core.views.auth import ERPLoginView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Auth
    path("accounts/login/", ERPLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),

    # Company FIRST (important)
    path("company/", include(("company.urls", "company"), namespace="company")),

    # Core business apps
    path("accounting/", include(("accounting.urls", "accounting"), namespace="accounting")),
    path("api/", include(("fiscal.urls", "fiscal"), namespace="fiscal")),
    path("sales/", include(("sales.urls", "sales"), namespace="sales")),
    path("purchases/", include(("purchases.urls", "purchases"), namespace="purchases")),
    path("inventory/", include(("inventory.urls", "inventory"), namespace="inventory")),
    path("reports/", include(("reports.urls", "reports"), namespace="reports")),

    # Submodules (each with namespace)
    path("products/", include(("products.urls", "products"), namespace="products")),
    path("customers/", include(("customers.urls", "customers"), namespace="customers")),
    path("suppliers/", include(("suppliers.urls", "suppliers"), namespace="suppliers")),

    # Core LAST (important)
    path("", include("core.urls")),
]
