from ulid import ULID


def generate_instance_id() -> str:
    """
    Generate a process-wide instance id in ULID format.

    ULID is 26 chars (Crockford Base32) and lexicographically sortable by time.
    """


    return str(ULID())


