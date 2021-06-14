from datetime import datetime, timedelta, timezone

import pytest
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_anonymous_user_can_access_resource_authorization_view(
    protected_url_resource_factory,
):
    raw_password = "test124"

    resource = protected_url_resource_factory(password=make_password(raw_password))
    client = APIClient()

    response = client.post(
        f"/api/protected/{str(resource.access_id)}/reveal/",
        data={"password": raw_password},
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_expired_resource_cannot_be_retrieved(lazy_resource_with_custom_created):
    current_time = datetime(2021, 6, 12, 12, 0, 0, tzinfo=timezone.utc)
    created = current_time - timedelta(hours=settings.RESOURCE_DEFAULT_TTL_HOURS + 1)
    resource = lazy_resource_with_custom_created(created)

    client = APIClient()
    response = client.post(
        f"/api/protected/{str(resource.access_id)}/reveal/",
    )

    assert response.status_code == 410
