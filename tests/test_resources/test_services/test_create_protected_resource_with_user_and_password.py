import io

import pytest
from resources.constants import TYPE_FILE, TYPE_URL
from resources.services import create_protected_resource_with_user_and_password
from resources.errors.internal_errors import RulesetViolation


@pytest.mark.django_db
def test_create_protected_url(user_factory):
    user = user_factory()
    password = "test_password"
    protected_url = "https://github.com"

    resource = create_protected_resource_with_user_and_password(
        user, password, protected_url=protected_url
    )

    assert resource.user == user
    assert resource.resource_type == TYPE_URL
    assert resource.protected_url == protected_url
    assert resource._password == password
    assert resource.visits == 0


@pytest.mark.django_db
def test_create_protected_file(user_factory, lazy_simple_in_memory_file):
    user = user_factory()
    password = "test_password"
    protected_file = lazy_simple_in_memory_file("file.txt", "content", "text/plain")
    resource = create_protected_resource_with_user_and_password(
        user, password, protected_file=protected_file
    )

    assert resource.user == user
    assert resource.resource_type == TYPE_FILE
    assert resource.protected_file.read() == b"content"
    assert resource._password == password
    assert resource.visits == 0


@pytest.mark.django_db
def test_cant_add_both_file_and_url(user_factory, lazy_simple_in_memory_file):
    protected_url = "https://github.com"
    protected_file = lazy_simple_in_memory_file("file.txt", "content", "text/plain")

    with pytest.raises(RulesetViolation):
        create_protected_resource_with_user_and_password(
            user_factory(),
            "test_password",
            protected_url=protected_url,
            protected_file=protected_file,
        )


@pytest.mark.django_db
def test_cant_create_resource_without_password(user_factory):

    with pytest.raises(RulesetViolation):
        create_protected_resource_with_user_and_password(
            user_factory(), "", protected_url="https://github.com"
        )


@pytest.mark.django_db
def test_anonymous_user_cant_create_resource(anonymous_user):
    password = "test_password"

    with pytest.raises(RulesetViolation):
        create_protected_resource_with_user_and_password(
            anonymous_user, "test_password", protected_url="https://github.com"
        )
