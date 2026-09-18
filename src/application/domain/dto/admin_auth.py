from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AdminLoginDto:
    id: str
    login: str
    first_name: str | None
    last_name: str | None
    role: str
    access_token: str
    refresh_token: str
    last_login_at: datetime | None = None
