from typing import Any, Mapping
from faststream.rabbit import RabbitBroker
from src.application.contracts import IQueueMessanger
from src.infrastructure.config import settings


class RabbitClient(IQueueMessanger):
    def __init__(self) -> None:
        self._broker = RabbitBroker(
            settings.RABBIT_URL,
        )
        self._connected = False

    async def connect(self) -> None:
        if self._connected:
            return
        await self._broker.connect()
        self._connected = True

    async def close(self) -> None:
        if not self._connected:
            return
        await self._broker.close()
        self._connected = False

    async def _ensure_connected(self) -> None:
        if not self._connected:
            await self.connect()

    async def publish_to_queue(
        self,
        queue: str,
        message: Any,
        *,
        persist: bool | None = None,
        headers: Mapping[str, Any] | None = None,
        correlation_id: str | None = None,
        message_id: str | None = None,
    ) -> None:
        await self._ensure_connected()

        await self._broker.publish(
            message,
            queue=queue,
            persist=settings.RABBIT_PUBLISH_PERSIST if persist is None else persist,
            headers=headers,
            correlation_id=correlation_id,
            message_id=message_id,
        )

    async def publish(
        self,
        message: Any,
        *,
        exchange: str,
        routing_key: str,
        persist: bool | None = None,
        headers: Mapping[str, Any] | None = None,
        correlation_id: str | None = None,
        message_id: str | None = None,
    ) -> None:
        await self._ensure_connected()

        await self._broker.publish(
            message,
            exchange=exchange,
            routing_key=routing_key,
            persist=settings.RABBIT_PUBLISH_PERSIST if persist is None else persist,
            headers=headers,
            correlation_id=correlation_id,
            message_id=message_id,
        )
