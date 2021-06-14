from string import ascii_letters, digits

from django.utils.crypto import get_random_string

ALLOWED_CHARS = ascii_letters + digits


def password_factory(length: int = 15, allowed_chars: str = ALLOWED_CHARS):
    return get_random_string(length=length, allowed_chars=allowed_chars)
