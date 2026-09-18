
from pydantic import BaseModel, field_validator
from src.application.domain.password_policy import validate_password_strength


class SetPasswordRequest(BaseModel):
    email: str | None = None
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)
