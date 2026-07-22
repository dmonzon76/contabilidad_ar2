"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core.views.auth import ERPLoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", ERPLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),


    # Company FIRST (important)
    path("company/", include(("company.urls", "company"), namespace="company")),

    # Other apps
    path("accounting/", include("accounting.urls")),
    path("api/", include("fiscal.urls")),
    path("sales/", include("sales.urls")),
    path("purchases/", include("purchases.urls")),
    path("inventory/", include(("inventory.urls", "inventory"), namespace="inventory")),
    path("reports/", include("reports.urls")),
    path("products/", include("products.urls")),
    path("customers/", include("customers.urls")),
    path("suppliers/", include("suppliers.urls")),









    # New apps
    path("customers/", include("customers.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("products/", include("products.urls")),

    # Core LAST (important)
    path("", include("core.urls")),
]



































