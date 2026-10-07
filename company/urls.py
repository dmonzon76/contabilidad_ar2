from django.urls import path

from company.views.activity import (
    activity_create,
    activity_delete,
    activity_edit,
    activity_list,
)
from company.views.company_views import (
    company_create,
    company_detail,
    company_edit,
    company_list,
)
from company.views.profile import (
    company_tax_profile_edit,
    company_tax_profile_view,
)
from company.views.select import (
    clear_select_modal_flag,
    select_company,
    select_company_list,
)
from company.views.users import (
    company_user_create,
    company_user_delete,
    company_user_edit,
    company_user_list,
)

app_name = "company"

urlpatterns = [
    # --- SELECTOR DE EMPRESAS ---
    path("select/", select_company_list, name="company_select_list"),
    path("select/", select_company_list, name="company_select"),
    path("select/<int:company_id>/", select_company, name="company_select_id"),
    path("set-active/<int:company_id>/", select_company, name="company_set_active"),
    path("set-active/<int:company_id>/", select_company, name="set_active_company"),
    path("clear-modal-flag/", clear_select_modal_flag, name="clear_select_modal_flag"),
    path("clear-modal-flag/", clear_select_modal_flag, name="company_clear_modal_flag"),
    # --- CRUD DE EMPRESAS ---
    path("", company_list, name="company_list"),
    path("new/", company_create, name="company_create"),
    path("<int:company_id>/edit/", company_edit, name="company_edit"),
    path("<int:company_id>/", company_detail, name="company_detail"),
    # --- ACTIVIDADES DE LA EMPRESA ---
    path("<int:company_id>/activities/", activity_list, name="company_activity_list"),
    path("<int:company_id>/activities/new/", activity_create, name="company_activity_create"),
    path("<int:company_id>/activities/<int:activity_id>/edit/", activity_edit, name="company_activity_edit"),
    path("<int:company_id>/activities/<int:activity_id>/delete/", activity_delete, name="company_activity_delete"),
    # --- PERFIL FISCAL ---
    path("<int:company_id>/tax-profile/", company_tax_profile_view, name="company_tax_profile"),
    path("<int:company_id>/tax-profile/edit/", company_tax_profile_edit, name="company_tax_profile_edit"),
    # --- USUARIOS Y ROLES ---
    path("<int:company_id>/users/", company_user_list, name="company_user_list"),
    path("<int:company_id>/users/new/", company_user_create, name="company_user_create"),
    path("<int:company_id>/users/<int:user_id>/edit/", company_user_edit, name="company_user_edit"),
    path("<int:company_id>/users/<int:user_id>/delete/", company_user_delete, name="company_user_delete"),
]
