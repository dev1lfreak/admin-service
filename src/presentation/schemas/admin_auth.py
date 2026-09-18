from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8)


class AdminLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    id: str
    login: str
    first_name: str | None
    last_name: str | None
    role: str


class AdminRefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=10)


class AdminRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class AdminMeResponse(BaseModel):
    id: str
    login: str
    first_name: str | None
    last_name: str | None
    role: str
