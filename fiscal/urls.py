from django.urls import path
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

app_name = "fiscal"

urlpatterns = [
    path("afip/", afip_activity_list, name="afip_activity_list"),
    path("afip/new/", afip_activity_create, name="afip_activity_create"),
    path("afip/<int:pk>/edit/", afip_activity_edit, name="afip_activity_edit"),

    path("company/", company_tax_profile, name="company_tax_profile"),

    path("thirdparty/", thirdparty_tax_list, name="thirdparty_tax_list"),
    path("thirdparty/<int:pk>/edit/", thirdparty_tax_edit, name="thirdparty_tax_edit"),
]
