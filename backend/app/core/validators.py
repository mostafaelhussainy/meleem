import re

from .exceptions.exceptions import InvalidPasswordException

def validate_password(v: str) -> str:
    if len(v) < 8:
        raise InvalidPasswordException("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', v):
        raise InvalidPasswordException("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', v):
        raise InvalidPasswordException("Password must contain at least one lowercase letter")
    if not re.search(r'\d', v):
        raise InvalidPasswordException("Password must contain at least one digit")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', v):
        raise InvalidPasswordException("Password must contain at least one special character")
    return v