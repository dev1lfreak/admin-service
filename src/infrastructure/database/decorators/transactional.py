from __future__ import annotations
from functools import wraps
from typing import Callable, Awaitable, TypeVar, ParamSpec


P = ParamSpec("P")
R = TypeVar("R")


def transactional(method: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @wraps(method)
    async def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
        async with self._unit_of_work:
            return await method(self, *args, **kwargs)
    return wrapper
