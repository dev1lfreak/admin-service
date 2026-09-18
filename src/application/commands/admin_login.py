from __future__ import annotations

from datetime import datetime, timezone

from src.application.abstractions import IUnitOfWork
from src.application.contracts import IHashService, IJwtService, ILogger
from src.application.domain.dto.admin_auth import AdminLoginDto
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.decorators import transactional


class AdminLoginCommand:
    def __init__(
        self,
        unit_of_work: IUnitOfWork,
        hash_service: IHashService,
        jwt_service: IJwtService,
        logger: ILogger,
    ):
        self._unit_of_work = unit_of_work
        self._hash_service = hash_service
        self._jwt_service = jwt_service
        self._logger = logger

    @transactional
    async def __call__(self, *, login: str, password: str) -> AdminLoginDto:
        login = (login or '').strip()
        if not login:
            raise ApplicationException(status_code=400, message='Login is required')
        admin = await self._unit_of_work.admin_user_repository.get_by_login(login)

        if not admin.is_active:
            raise ApplicationException(status_code=403, message='Admin account is inactive')

        ok = await self._hash_service.verify(plain_value=password, hashed_value=admin.password_hash)
        if not ok:
            self._logger.warning(f'Admin login failed for {login}')
            raise ApplicationException(status_code=401, message='Invalid credentials')

        now = datetime.now(timezone.utc)
        await self._unit_of_work.admin_user_repository.update_last_login(admin.id, last_login_at=now)

        access_token = await self._jwt_service.create_access_token(user_id=admin.id, role=admin.role)
        refresh_token = await self._jwt_service.create_refresh_token(user_id=admin.id, role=admin.role)

        self._logger.info(f'Admin logged in admin_user_id={admin.id}')

        return AdminLoginDto(
            id=admin.id,
            login=admin.login,
            first_name=admin.first_name,
            last_name=admin.last_name,
            role=admin.role,
            access_token=access_token,
            refresh_token=refresh_token,
            last_login_at=now,
        )
