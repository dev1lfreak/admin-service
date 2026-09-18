from src.application.abstractions import IUnitOfWork
from src.application.contracts import IJwtService, ILogger
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.decorators import transactional


class AdminJwtRefreshCommand:
    def __init__(
        self,
        unit_of_work: IUnitOfWork,
        jwt_service: IJwtService,
        logger: ILogger,
    ):
        self._unit_of_work = unit_of_work
        self._jwt_service = jwt_service
        self._logger = logger

    @transactional
    async def __call__(self, *, refresh_token: str) -> tuple[str, str]:
        payload = await self._jwt_service.decode_refresh_token(refresh_token)
        admin = await self._unit_of_work.admin_user_repository.get_by_id(payload.sub)

        if not admin.is_active:
            raise ApplicationException(status_code=403, message='Admin account is inactive')

        access = await self._jwt_service.create_access_token(user_id=admin.id, role=admin.role)
        refresh = await self._jwt_service.create_refresh_token(user_id=admin.id, role=admin.role)
        self._logger.info(f'Admin tokens refreshed admin_user_id={admin.id}')
        return access, refresh
