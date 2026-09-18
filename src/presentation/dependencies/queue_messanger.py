from functools import lru_cache
from src.application.contracts import IQueueMessanger
from src.infrastructure.messanger import RabbitClient


@lru_cache(maxsize=1)
def get_rabbit() -> IQueueMessanger:
    return RabbitClient()
