from django.urls import path

from . import views

app_name = "locations_api"

urlpatterns = [
    path("prefs/", views.pref_list, name="pref_list"),
]
