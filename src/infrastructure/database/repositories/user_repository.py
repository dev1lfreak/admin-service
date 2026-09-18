from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.application.abstractions.repositories import IUserRepository
from src.application.contracts import ILogger
from src.application.domain.entities import UserEntity
from src.application.domain.entities.party_search import PartySearchEntity
from src.application.domain.enums.account_type import AccountType
from src.application.domain.exceptions import InternalServerException, ApplicationException
from src.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, user: UserModel) -> UserEntity:
        return UserEntity(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            birth_date=user.birth_date,
            encrypted_mnemonic=user.encrypted_mnemonic,
            phone=user.phone,
            passport_data=user.passport_data,
            inn=user.inn,
            erc20=user.erc20,
            avatar_link=user.avatar_link,
            kyc_verified=user.kyc_verified,
            is_deleted=user.is_deleted,
            created_at=user.created_at,
            updated_at=user.updated_at,
            kyc_verified_at=user.kyc_verified_at,
            account_type=user.account_type,
            provisioned_by=user.provisioned_by,
            provisioned_at=user.provisioned_at,
        )
    
    async def get_by_id(self, user_id: str) -> UserEntity:
        try:
            user = await self._get_user(user_id)
            return self._to_entity(user)
        except ApplicationException:
            raise
        except SQLAlchemyError as exception:
            self._logger.exception(str(exception))
            raise InternalServerException(message=f'Database error: {str(exception)}')

    async def create_legal_entity_user(
        self,
        *,
        email: str,
        password_hash: str,
        provisioned_by: str,
        provisioned_at: datetime,
        kyc_verified: bool,
        kyc_verified_at: datetime,
    ) -> UserEntity:
        user = UserModel(
            email=email,
            password_hash=password_hash,
            account_type=AccountType.LEGAL_ENTITY,
            provisioned_by=provisioned_by,
            provisioned_at=provisioned_at,
            kyc_verified=kyc_verified,
            kyc_verified_at=kyc_verified_at,
        )
        self._session.add(user)
        try:
            await self._session.flush()
            return self._to_entity(user)
        except IntegrityError:
            raise ApplicationException(status_code=409, message='User with this email already exists')
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')
        
    async def _get_user(self, user_id: str) -> UserModel:
        stmt = (
            select(UserModel)
            .where(
                UserModel.id == user_id,
                UserModel.is_deleted.is_(False),
            )
        )
        result = await self._session.execute(stmt)
        user: UserModel | None = result.scalar_one_or_none()
        if user is None:
            self._logger.warning(f'User not found with user_id {user_id}')
            raise ApplicationException(status_code=404, message='User not found')
        return user

    async def _update_field(self, user_id: str, **fields: object) -> UserEntity:
        try:
            user = await self._get_user(user_id)
            for key, value in fields.items():
                setattr(user, key, value)
            await self._session.flush()
            await self._session.refresh(user)
            return self._to_entity(user)
        except ApplicationException:
            raise
        except SQLAlchemyError as exception:
            self._logger.exception(str(exception))
            raise InternalServerException(message=f'Database error: {str(exception)}')
    
    async def set_password(self, user_id: str, password_hash: str) -> UserEntity:
        return await self._update_field(user_id, password_hash=password_hash)

    async def get_user_by_email(self, email: str) -> UserEntity:
        try:
            stmt = select(UserModel).where(UserModel.email == email, UserModel.is_deleted.is_(False))
            result = await self._session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise ApplicationException(status_code=404, message='User not found')
            return self._to_entity(user)
        except ApplicationException:
            raise
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(UserModel.id).where(UserModel.email == email, UserModel.is_deleted.is_(False)).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def _search_filter(self, search: str | None):
        if not search or not search.strip():
            return None

        pattern = f'%{search.strip()}%'
        return or_(
            UserModel.id.ilike(pattern),
            UserModel.email.ilike(pattern),
            UserModel.last_name.ilike(pattern),
            UserModel.first_name.ilike(pattern),
            UserModel.middle_name.ilike(pattern),
            UserModel.phone.ilike(pattern),
            UserModel.inn.ilike(pattern),
        )
    
    async def list_all(
        self,
        *,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> list[UserEntity]:
        stmt = (
            select(UserModel)
            .where(UserModel.is_deleted.is_(False))
            .order_by(UserModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return [self._to_entity(m) for m in res.scalars().all()]

    def _individual_search_filter(self, query: str):
        pattern = f'%{query.strip()}%'
        full_name = func.concat_ws(
            ' ',
            UserModel.last_name,
            UserModel.first_name,
            UserModel.middle_name,
        )
        return or_(
            UserModel.id.ilike(pattern),
            UserModel.email.ilike(pattern),
            UserModel.last_name.ilike(pattern),
            UserModel.first_name.ilike(pattern),
            UserModel.middle_name.ilike(pattern),
            UserModel.phone.ilike(pattern),
            UserModel.passport_data.ilike(pattern),
            UserModel.inn.ilike(pattern),
            UserModel.erc20.ilike(pattern),
            full_name.ilike(pattern),
        )

    def _to_search_entity(self, user: UserModel) -> PartySearchEntity:
        name = ' '.join(
            part for part in (user.last_name, user.first_name, user.middle_name)
            if part
        ) or None
        return PartySearchEntity(
            id=user.id,
            account_type=user.account_type,
            user_id=user.id,
            email=user.email,
            name=name,
            inn=user.inn,
            phone=user.phone,
            status=None,
            kyc_verified=user.kyc_verified,
            created_at=user.created_at,
        )

    async def search_individuals(self, *, query: str, limit: int, offset: int) -> list[PartySearchEntity]:
        stmt = (
            select(UserModel)
            .where(
                UserModel.is_deleted.is_(False),
                UserModel.account_type == AccountType.INDIVIDUAL,
                self._individual_search_filter(query),
            )
            .order_by(UserModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return [self._to_search_entity(user) for user in result.scalars().all()]

    async def count_individuals(self, *, query: str) -> int:
        stmt = (
            select(func.count(UserModel.id))
            .where(
                UserModel.is_deleted.is_(False),
                UserModel.account_type == AccountType.INDIVIDUAL,
                self._individual_search_filter(query),
            )
        )
        result = await self._session.execute(stmt)
        return int(result.scalar_one())
    
    async def count_all(self, *, search: str | None = None) -> int:
        stmt = (
            select(func.count(UserModel.id))
            .where(UserModel.is_deleted.is_(False))
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())
