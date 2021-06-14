from collections import defaultdict

from rest_framework.exceptions import ValidationError


class RulesetValidationAPIError(ValidationError):
    def __init__(self, detail, code=None):
        self.detail = defaultdict(list)

        for error in detail:
            key = error.field or "errors"
            self.detail[key].append(error.error_msg)
