from abc import ABC, abstractmethod
from src.application.domain.dto import UserCreatedDto, UserLoginDto


class IUserService(ABC):

    @abstractmethod
    async def registration(self, email: str, password: str) -> UserCreatedDto:
        raise NotImplementedError


    @abstractmethod
    async def login(self, email: str, password: str) -> UserLoginDto:
        raise NotImplementedError