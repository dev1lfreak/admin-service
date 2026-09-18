import bcrypt
from src.application.contracts import IHashService, ILogger


class HashService(IHashService):

    def __init__(self, logger: ILogger):
        self._logger = logger

    async def hash(self, value: str) -> str:
        hashed_value = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        self._logger.info(f'Hash value {hashed_value.decode()}')
        return hashed_value.decode()

    async def verify(self, hashed_value: str, plain_value: str) -> bool:
        self._logger.info(f'Hash value {hashed_value[:10]}')
        return bcrypt.checkpw(plain_value.encode(), hashed_value.encode())