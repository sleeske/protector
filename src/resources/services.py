from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from resources.models import ProtectedResource


def create_protected_resource_with_username_and_password(
    user, raw_password, **kwargs
) -> ProtectedResource:
    kwargs["password"] = make_password(raw_password)
    resource = ProtectedResource.objects.create(user=user, **kwargs)
    resource._password = raw_password
    return resource


def increment_visitors_count(resource: ProtectedResource) -> ProtectedResource:
    resource.visits += 1
    resource.save(update_fields=["visits"])
    return resource


def change_resource_password(
    resource: ProtectedResource, raw_password: str
) -> ProtectedResource:
    resource.password = make_password(raw_password)
    resource.save(update_fields=["password"])
    return resource


def is_resource_expired(
    resource: ProtectedResource,
    date_time: Optional[datetime] = None,
    resource_ttl: Optional[timedelta] = None,
) -> bool:
    if not date_time:
        date_time = timezone.localtime()

    if not resource_ttl:
        resource_ttl = settings.RESOURCE_DEFAULT_TTL

    return resource.created + resource_ttl < date_time
