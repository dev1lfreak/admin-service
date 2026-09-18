from src.application.abstractions import IUnitOfWork
from src.application.contracts import IHashService, ILogger
from src.application.domain.exceptions import ApplicationException, BadRequestException
from src.infrastructure.database.decorators import transactional


class SetPasswordCommand:
    def __init__(
            self,
            unit_of_work: IUnitOfWork, 
            hash_service: IHashService, 
            logger: ILogger
    ):
        self._unit_of_work = unit_of_work
        self._hash_service = hash_service
        self._logger = logger

    @transactional
    async def __call__(
            self,
            password: str,
            email: str | None = None, 
            user_id: str | None = None,
        ) -> bool:
        try:
            password_hash = await self._hash_service.hash(password)

            if email == None and user_id == None:
                raise BadRequestException('An email is required')

            if email != None:
                user = await self._unit_of_work.user_repository.get_user_by_email(email)
                user_id = user.id
            await self._unit_of_work.user_repository.set_password(
                user_id=user_id,
                password_hash=password_hash,
            )
            self._logger.info(f'Set password for user {user_id}')
            return True
        except ApplicationException:
            raise
