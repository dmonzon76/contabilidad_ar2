from django.urls import path
from company.views.select import (
    select_company_list,
    select_company,
    clear_select_modal_flag,
)
from company.views.company_views import (
    company_list,
    company_create,
    company_edit,
    company_detail,
)

app_name = "company"

urlpatterns = [
    # Selector
    path("select/", select_company_list, name="company_select_list"),
    path("select/", select_company_list, name="company_select"),
    path("select/<int:company_id>/", select_company, name="company_select_id"),
    path("set-active/<int:company_id>/", select_company, name="set_active_company"),
    path("clear-modal-flag/", clear_select_modal_flag, name="clear_select_modal_flag"),

    # CRUD de Empresas
    path("", company_list, name="company_list"),
    path("new/", company_create, name="company_create"),
    path("<int:company_id>/edit/", company_edit, name="company_edit"),
    path("<int:company_id>/", company_detail, name="company_detail"),
]