from typing import List


class ResourceError(Exception):
    pass


class RuleViolation(ResourceError):
    field = None
    error_msg = ""


class AnonymousUserNotAuthorized(RuleViolation):
    error_msg = "Anonymous user can't add a resource."


class PasswordNoneOrEmpty(RuleViolation):
    error_msg = "Can't create a resource without a password."


class TooManyFieldsProvided(RuleViolation):
    error_msg = "Provide an URL or a file to protect."


class NotEnoughFieldsProvided(RuleViolation):
    error_msg = "Provice either an URL or a file to protect, not both."


class RulesetViolation(ResourceError):
    def __init__(self, errors: List[RuleViolation], *args):
        super().__init__(*args)
        self.errors = errors


class ResourcePasswordMismatch(ResourceError):
    field = "password"
    error_msg = "Invalid password."
