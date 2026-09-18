from functools import lru_cache
from src.application.contracts import ILogger
from src.infrastructure.logger import logger

@lru_cache
def get_logger() -> ILogger:
    return logger