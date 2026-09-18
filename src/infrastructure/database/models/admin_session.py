from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import AuditTimestampsMixin, UlidPrimaryKeyMixin


class AdminSessionModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin):
    __tablename__ = 'admin_sessions'

    sid: Mapped[str] = mapped_column(
        String(26),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(ULID()),
    )
    admin_user_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('admin_users.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    device_id: Mapped[str] = mapped_column(String(26), nullable=False, index=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    first_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refresh_jti_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


Index('ux_admin_sessions_user_device', AdminSessionModel.admin_user_id, AdminSessionModel.device_id, unique=True)
