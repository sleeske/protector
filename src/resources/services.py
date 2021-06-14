from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from resources.errors.internal_errors import ResourcePasswordMismatch
from resources.models import ProtectedResource
from resources.validators.decorators import ruleset
from resources.validators.rulesets import (
    change_resource_password_ruleset,
    create_protected_resource_with_user_and_password_ruleset,
)


@ruleset(create_protected_resource_with_user_and_password_ruleset)
def create_protected_resource_with_user_and_password(
    user, raw_password, **kwargs
) -> ProtectedResource:
    kwargs["password"] = make_password(raw_password)
    resource = ProtectedResource.objects.create(user=user, **kwargs)
    resource._password = raw_password
    return resource


def increment_visitors_count(resource) -> ProtectedResource:
    resource.visits += 1
    resource.save(update_fields=["visits"])
    return resource


def check_resource_password(resource, password) -> None:
    if not check_password(password, resource.password):
        raise ResourcePasswordMismatch


@ruleset(change_resource_password_ruleset)
def change_resource_password(resource, raw_password) -> ProtectedResource:
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
