from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    sub: str
    type: str
    role: str | None = None
    iat: int
    nbf: int
    exp: int
    iss: str | None = None
    aud: str | None = None


class RefreshTokenPayload(BaseModel):
    sub: str
    type: str
    role: str
    iat: int
    nbf: int
    exp: int
    iss: str | None = None
    aud: str | None = None


class AdminAuthContext(BaseModel):
    admin_user_id: str
    role: str
