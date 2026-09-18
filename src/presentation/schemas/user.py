from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: str | None = Field(None, description='Идентификатор пользователя')
    email: str | None = Field(None, description='Email')
    first_name: str | None = Field(None, description='Имя')
    middle_name: str | None = Field(None, description='Отчество')
    last_name: str | None = Field(None, description='Фамилия')
    birth_date: date | None = Field(None, description='Дата рождения')
    phone: str | None = Field(None, description='Телефон')
    passport_data: str | None = Field(None, description='Паспортные данные')
    inn: str | None = Field(None, description='ИНН')
    avatar_link: str | None = Field(None, description='HTTPS-ссылка на текущий аватар в хранилище')
    account_type: str | None = Field(None, description='Тип аккаунта')
    kyc_verified: bool | None = Field(None, description='Признак пройденного KYC')
    is_deleted: bool | None = Field(None, description='Удалён ли аккаунт')
    created_at: datetime | None = Field(None, description='Время создания записи')
    updated_at: datetime | None = Field(None, description='Время последнего обновления')
    kyc_verified_at: datetime | None = Field(None, description='Время подтверждения KYC')


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
