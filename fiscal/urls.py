from django.urls import path
from .api import afip_search

urlpatterns = [
    path("afip/search/", afip_search, name="afip_search"),
]
