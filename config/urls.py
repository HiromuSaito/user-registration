from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from user_registration.views import spa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user_registration.locations.api.urls")),
    path("api/", include("user_registration.accounts.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("app/", spa, name="spa"),
    path("app/<path:path>", spa, name="spa"),
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("spa", kwargs={"path": "signup/"})),
    ),
    path("", include("user_registration.accounts.urls")),
]
