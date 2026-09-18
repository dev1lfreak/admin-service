from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AdminUserEntity:
    id: str
    login: str
    password_hash: str
    first_name: str | None
    last_name: str | None
    role: str
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
