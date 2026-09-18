from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

@dataclass
class PartySearchEntity:
    id: str
    account_type: str
    user_id: str
    email: str | None
    name: str | None
    inn: str | None
    phone: str | None
    status: str | None = None
    kyc_verified: bool | None = None
    created_at: datetime | None = None