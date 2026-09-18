from fastapi import Depends
from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.context import async_session_maker
from src.infrastructure.logger import get_logger


def get_unit_of_work(logger: ILogger = Depends(get_logger)) -> IUnitOfWork:
    return UnitOfWork(session_factory=async_session_maker, logger=logger)