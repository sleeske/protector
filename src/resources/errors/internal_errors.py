from typing import List


class ResourceError(Exception):
    pass


class RuleViolation(ResourceError):
    def __init__(self, field, error_msg, *args):
        super().__init__(*args)
        self.field = field
        self.error_msg = error_msg

    def __str__(self):
        return f"{self.field}: {self.msg}"


class RulesetViolation(ResourceError):
    def __init__(self, errors: List[RuleViolation], *args):
        super().__init__(*args)
        self.errors = errors


class ResourcePasswordMismatch(ResourceError):
    field = "password"
    error_msg = "Invalid password."
