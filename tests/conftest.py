from datetime import datetime

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_factoryboy import register
from resources.models import ProtectedResource

from .factories.resource import ProtectedURLResourceFactory
from .factories.user import UserFactory

register(UserFactory)
register(ProtectedURLResourceFactory)


@pytest.fixture
def lazy_simple_in_memory_file():
    def wrapper(file_name, content, content_type):
        return SimpleUploadedFile(file_name, content.encode(), content_type)

    return wrapper


@pytest.fixture
def lazy_resource_with_custom_created(protected_url_resource_factory):
    def wrapper(created: datetime):
        resource = protected_url_resource_factory()
        ProtectedResource.objects.filter(pk=resource.pk).update(created=created)
        resource.refresh_from_db()
        return resource

    return wrapper


@pytest.fixture
def anonymous_user():
    return AnonymousUser()
