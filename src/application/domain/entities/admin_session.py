from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AdminSessionEntity:
    sid: str
    admin_user_id: str
    device_id: str
    revoked_at: datetime | None
    last_seen_at: datetime
    refresh_jti_hash: str | None
    refresh_expires_at: datetime | None
    user_agent: str | None = None
    first_ip: str | None = None
    last_ip: str | None = None
