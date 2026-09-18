import re

SPECIAL_CHARS = '!@#$%^&*()_+-=.,:;?/[]{}<>'


def validate_password_strength(password: str) -> str:
    if re.search(r'\s', password):
        raise ValueError('Password must not contain whitespace')
    if len(password) < 12:
        raise ValueError('Password must be at least 12 characters')
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')
    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one digit')
    if not any(c in SPECIAL_CHARS for c in password):
        raise ValueError(
            'Password must contain at least one special character from: !@#$%^&*()_+-=.,:;?/[]{}<>'
        )
    return password
