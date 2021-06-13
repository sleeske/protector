from django.urls import path
from resources.views import api_views


urlpatterns = [
    path(
        "protected/add/",
        api_views.ProtectedResourceCreateAPIView.as_view(),
        name="api-create",
    ),
    path(
        "protected/<uuid:access_id>/reveal/",
        api_views.ProtectedResourceAuthorizationAPIView.as_view(),
        name="api-authorize",
    ),
    path(
        "protected/stats/", api_views.ProtectedResourceStats.as_view(), name="api-stats"
    ),
]
