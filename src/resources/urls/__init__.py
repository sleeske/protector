from django.urls import path
from django.urls.conf import include

from resources.urls.api_urls import urlpatterns as api_patterns
from resources.views import views

app_name = "resources"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "protected/add/",
        views.ProtectedResourceCreateView.as_view(),
        name="create",
    ),
    path(
        "protected/<uuid:access_id>/reveal/",
        views.ProtectedResourceAuthorizationView.as_view(),
        name="authorize",
    ),
    path(
        "redirect/<uuid:pk>/",
        views.ProtectedURLRedirectView.as_view(),
        name="redirect",
    ),
    path(
        "download/<uuid:pk>/",
        views.ProtectedFileDownloadView.as_view(),
        name="download",
    ),
    path("api/", include(api_patterns)),
]
