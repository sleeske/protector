from datetime import datetime, timedelta, timezone

import pytest

from resources.services import is_resource_expired


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("created", "current_time", "ttl", "expected"),
    (
        (
            datetime(2021, 6, 12, 10, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 6, 12, 20, 0, 0, tzinfo=timezone.utc),
            timedelta(hours=11),
            False,
        ),
        (
            datetime(2021, 6, 12, 10, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 6, 12, 20, 0, 0, tzinfo=timezone.utc),
            timedelta(hours=10),
            False,
        ),
        (
            datetime(2021, 6, 12, 10, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 6, 12, 20, 0, 0, tzinfo=timezone.utc),
            timedelta(hours=9),
            True,
        ),
    ),
)
def test_resource_ttl_windows(
    created, current_time, ttl, expected, lazy_resource_with_custom_created
):
    resource = lazy_resource_with_custom_created(created)
    assert is_resource_expired(resource, current_time, ttl) is expected
