from typing import Protocol, Optional, Callable
from src.application.domain.enums.log_format import LogFormat
from src.application.domain.enums.log_level import LogLevel


class ILogger(Protocol):
    """Interface for synchronous logger with ContextVar support for trace_id."""

    log_format: LogFormat
    min_level: LogLevel
    id_generator: Optional[Callable[[], str]]
    instance_id: str

    def set_format(self, log_format: LogFormat) -> None:
        """Set log format using LogFormat enum"""
        ...

    def set_min_level(self, level: LogLevel) -> None:
        """Set minimum log level"""
        ...

    def new_trace_id(self) -> str:
        """Create and set new trace_id in context"""
        ...

    def set_trace_id(self, trace_id: str) -> None:
        """Set existing trace_id in context"""
        ...

    def get_trace_id(self) -> str:
        """Get current trace_id from context"""
        ...

    def clear_trace_id(self) -> None:
        """Clear the trace_id in the context"""
        ...

    def set_instance_id(self, instance_id: str) -> None:
        """Set service instance id (ULID recommended)"""
        ...

    def get_instance_id(self) -> str:
        """Get current service instance id"""
        ...

    def debug(self, message: str) -> None:
        """Log debug message"""
        ...

    def info(self, message: str) -> None:
        """Log info message"""
        ...

    def warning(self, message: str) -> None:
        """Log warning message"""
        ...

    def error(self, message: str) -> None:
        """Log error message"""
        ...

    def critical(self, message: str) -> None:
        """Log critical message"""
        ...

    def exception(self, message: str) -> None:
        """Log exception with traceback"""
        ...