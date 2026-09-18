from ulid import ULID


def new_ulid() -> str:
    return str(ULID())


def is_valid_ulid(value: str | None) -> bool:
    if not value:
        return False
    try:
        ULID.parse(value)
        return True
    except ValueError:
        return False
