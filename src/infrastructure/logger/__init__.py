from src.application.contracts import ILogger
from src.application.domain.enums import LogFormat
from src.application.domain.enums import LogLevel
from src.infrastructure.config.settings import settings
from src.infrastructure.logger.logger import Logger

log_levels = {
    'DEBUG': LogLevel.DEBUG,
    'INFO': LogLevel.INFO,
    'WARNING': LogLevel.WARNING,
    'ERROR': LogLevel.ERROR,
    'CRITICAL': LogLevel.CRITICAL,
    'EXCEPTION': LogLevel.EXCEPTION,
}

log_formats = {
    'JSON': LogFormat.JSON,
    'TEXT': LogFormat.TEXT,
}

logger = Logger(
    min_level=log_levels.get(settings.LOG_LEVEL, LogLevel.INFO),
    log_format=log_formats.get(settings.LOG_FORMAT, LogFormat.JSON),
)


def get_logger() -> ILogger:
    return logger
