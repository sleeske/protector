from resources.validators.rules import (
    validate_either_protected_url_or_file_present,
    validate_password_is_not_none_or_empty,
    validate_user_is_not_anonymous,
)
from functools import partial


def create_protected_resource_with_user_and_password_ruleset(
    user, raw_password, **kwargs
):
    return [
        partial(validate_user_is_not_anonymous, user=user),
        partial(validate_password_is_not_none_or_empty, password=raw_password),
        partial(
            validate_either_protected_url_or_file_present,
            protected_url=kwargs.get("protected_url"),
            protected_file=kwargs.get("protected_file"),
        ),
    ]


def change_resource_password_ruleset(resource, raw_password):
    return [partial(validate_password_is_not_none_or_empty, password=raw_password)]
