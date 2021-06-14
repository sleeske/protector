from functools import wraps
from resources.errors.internal_errors import RulesetViolation, RuleViolation


def ruleset(ruleset_factory):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            errors = []

            rules = ruleset_factory(*args, **kwargs)
            for rule in rules:
                try:
                    rule()
                except RuleViolation as e:
                    errors.append(e)

            if errors:
                raise RulesetViolation(errors)

            return func(*args, **kwargs)

        return inner

    return wrapper
