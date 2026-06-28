from django.urls import path

from fiscal.views.afip_activity import (
    afip_activity_list,
    afip_activity_create,
    afip_activity_edit,
    afip_activity_delete,
)

from fiscal.views.thirdparty_tax import (
    thirdparty_tax_list,
    thirdparty_tax_create,
    thirdparty_tax_edit,
    thirdparty_tax_delete,
)

from fiscal.views.company_tax import (
    company_tax_profile_view,
    company_tax_profile_edit,
)
app_name = "fiscal"

urlpatterns = [

    # AFIP Activities
    path("activities/", afip_activity_list, name="afip_activity_list"),
    path("activities/new/", afip_activity_create, name="afip_activity_create"),
    path("activities/<int:activity_id>/edit/", afip_activity_edit, name="afip_activity_edit"),
    path("activities/<int:activity_id>/delete/", afip_activity_delete, name="afip_activity_delete"),

    # Third Party Tax Profiles
    path("thirdparty/", thirdparty_tax_list, name="thirdparty_tax_list"),
    path("thirdparty/new/", thirdparty_tax_create, name="thirdparty_tax_create"),
    path("thirdparty/<int:profile_id>/edit/", thirdparty_tax_edit, name="thirdparty_tax_edit"),
    path("thirdparty/<int:profile_id>/delete/", thirdparty_tax_delete, name="thirdparty_tax_delete"),

    # Company Tax Profile
    path("company/", company_tax_profile_view, name="company_tax_profile"),
    path("company/edit/", company_tax_profile_edit, name="company_tax_profile_edit"),
]
