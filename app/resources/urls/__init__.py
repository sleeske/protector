from django.urls import path
from django.urls.conf import include

from resources.urls.api_urls import urlpatterns as api_patterns
from resources.views import template_views

app_name = "resources"

urlpatterns = [
    path("", template_views.index, name="index"),
    path(
        "protected/add/",
        template_views.ProtectedResourceCreateView.as_view(),
        name="create",
    ),
    path(
        "protected/<uuid:access_id>/reveal/",
        template_views.ProtectedResourceAuthorizationView.as_view(),
        name="authorize",
    ),
    path(
        "redirect/<uuid:pk>/",
        template_views.ProtectedURLRedirectView.as_view(),
        name="redirect",
    ),
    path(
        "download/<uuid:pk>/",
        template_views.ProtectedFileDownloadView.as_view(),
        name="download",
    ),
    path("api/", include(api_patterns)),
]
