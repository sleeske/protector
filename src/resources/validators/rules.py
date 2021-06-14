from resources.errors.internal_errors import (
    AnonymousUserViolation,
    EmptyPasswordViolation,
    TooManyResourcesProvidedViolation,
    NotEnoughResourcesProvidedViolation,
)


def validate_user_is_not_anonymous(user):
    if user and user.is_anonymous:
        raise AnonymousUserViolation


def validate_password_is_not_none_or_empty(password):
    if password is None or str(password) == "":
        raise EmptyPasswordViolation


def validate_either_protected_url_or_file_present(
    protected_url=None, protected_file=None
):
    if not protected_url and not protected_file:
        raise TooManyResourcesProvidedViolation

    if protected_url and protected_file:
        raise NotEnoughResourcesProvidedViolation
