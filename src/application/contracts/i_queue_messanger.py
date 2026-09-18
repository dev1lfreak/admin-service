from abc import ABC, abstractmethod
from typing import Mapping, Any


class IQueueMessanger(ABC):

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish_to_queue(
            self,
            queue: str,
            message: Any,
            *,
            persist: bool = True,
            headers: Mapping[str, Any] | None = None,
            correlation_id: str | None = None,
            message_id: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish(
            self,
            message: Any,
            *,
            exchange: str,
            routing_key: str,
            persist: bool = True,
            headers: Mapping[str, Any] | None = None,
            correlation_id: str | None = None,
            message_id: str | None = None,
    ) -> None:
        raise NotImplementedError