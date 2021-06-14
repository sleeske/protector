from resources.errors.internal_errors import RuleViolation


def validate_user_is_not_anonymous(user):
    if user and user.is_anonymous:
        raise RuleViolation(None, "Anonymous user can't add a resource.")


def validate_password_is_not_none_or_empty(password):
    if password is None or str(password) == "":
        raise RuleViolation(None, "Can't create a resource without a password.")


def validate_either_protected_url_or_file_present(
    protected_url=None, protected_file=None
):
    if not protected_url and not protected_file:
        raise RuleViolation(None, "Provide an URL or a file to protect.")

    if protected_url and protected_file:
        raise RuleViolation(
            None, "Provice either an URL or a file to protect, not both."
        )
