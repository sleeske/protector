from resources.errors.internal_errors import (
    AnonymousUserNotAuthorized,
    PasswordNoneOrEmpty,
    TooManyFieldsProvided,
    NotEnoughFieldsProvided,
)


def validate_user_is_not_anonymous(user):
    if user and user.is_anonymous:
        raise AnonymousUserNotAuthorized


def validate_password_is_not_none_or_empty(password):
    if password is None or str(password) == "":
        raise PasswordNoneOrEmpty


def validate_either_protected_url_or_file_present(
    protected_url=None, protected_file=None
):
    if not protected_url and not protected_file:
        raise TooManyFieldsProvided

    if protected_url and protected_file:
        raise NotEnoughFieldsProvided
