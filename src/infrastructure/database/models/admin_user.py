from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import AuditTimestampsMixin, UlidPrimaryKeyMixin


class AdminUserModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin):
    __tablename__ = 'admin_users'

    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False, server_default='operator', default='operator')
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true', default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
