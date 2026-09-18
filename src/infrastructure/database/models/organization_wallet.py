from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import UlidPrimaryKeyMixin


class OrganizationWalletModel(Base, UlidPrimaryKeyMixin):
    __tablename__ = 'organization_wallets'

    organization_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('legal_entities.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    chain: Mapped[str] = mapped_column(String(16), nullable=False)
    address: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    derivation_path: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
