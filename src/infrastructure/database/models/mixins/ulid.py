from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID


class UlidPrimaryKeyMixin:

    id: Mapped[str] = mapped_column(String(26), primary_key=True, default=lambda: str(ULID()))
