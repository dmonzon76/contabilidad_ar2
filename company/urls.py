from django.urls import path

from company.views.select import (
    select_company,
    set_active_company,
    clear_select_modal_flag,
)

from company.views.company_views import (
    company_list,
    company_create,
    company_detail,
)

from company.views.activity import (
    activity_list,
    activity_create,
    activity_edit,
    activity_delete,
)

from company.views.users import (
    company_user_list,
    company_user_create,
    company_user_edit,
    company_user_delete,
)

from company.views.profile import (
    company_tax_profile_view,
    company_tax_profile_edit,
)

app_name = "company"

urlpatterns = [
    # ============================================================
    # COMPANY SELECTOR
    # ============================================================
    path("select/", select_company, name="company_select"),
    path("select/<int:company_id>/", set_active_company, name="company_set_active"),
    path("select/clear-flag/", clear_select_modal_flag, name="company_clear_modal_flag"),

    # ============================================================
    # COMPANY CRUD
    # ============================================================
    path("", company_list, name="company_list"),
    path("new/", company_create, name="company_create"),
    path("<int:company_id>/", company_detail, name="company_detail"),

    # ============================================================
    # ACTIVITIES
    # ============================================================
    path("<int:company_id>/activities/", activity_list, name="company_activity_list"),
    path("<int:company_id>/activities/new/", activity_create, name="company_activity_create"),
    path("<int:company_id>/activities/<int:activity_id>/edit/", activity_edit, name="company_activity_edit"),
    path("<int:company_id>/activities/<int:activity_id>/delete/", activity_delete, name="company_activity_delete"),

    # ============================================================
    # TAX PROFILE
    # ============================================================
    path("<int:company_id>/tax-profile/", company_tax_profile_view, name="company_tax_profile"),
    path("<int:company_id>/tax-profile/edit/", company_tax_profile_edit, name="company_tax_profile_edit"),

    # ============================================================
    # USERS & ROLES
    # ============================================================
    path("<int:company_id>/users/", company_user_list, name="company_user_list"),
    path("<int:company_id>/users/new/", company_user_create, name="company_user_create"),
    path("<int:company_id>/users/<int:user_id>/edit/", company_user_edit, name="company_user_edit"),
    path("<int:company_id>/users/<int:user_id>/delete/",company_user_delete, name="company_user_delete"),
]





