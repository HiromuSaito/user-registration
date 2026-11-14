from django.urls import path

from . import views

app_name = "accounts_api"

urlpatterns = [
    path("users/", views.user_create, name="user_create"),
]
