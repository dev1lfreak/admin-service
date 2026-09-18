from __future__ import annotations
from typing import Optional
from contextvars import Token
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from ulid import ULID
from src.application.contracts import ILogger
from src.infrastructure.config import settings
from src.infrastructure.context_vars import trace_id_var


class TraceIDMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        logger: ILogger,
        response_header_name: str = "X-Trace-ID",
        attach_response_header: bool = True,
    ) -> None:
        self.app = app
        self.logger = logger
        self.response_header_name = response_header_name
        self.attach_response_header = attach_response_header

    def _is_excluded(self, path: str) -> bool:
        return any(path == p or path.startswith(p.rstrip("/") + "/") for p in settings.EXCLUDED_PATHS)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)

        if self._is_excluded(request.url.path):
            await self.app(scope, receive, send)
            return

        trace_id = request.headers.get("X-Trace-ID") or request.headers.get("X-Request-ID")
        if not trace_id:
            trace_id = str(ULID())

        request.state.trace_id = trace_id

        token: Token = trace_id_var.set(trace_id)

        self.logger.debug(f"Request started: {request.method} {request.url} - TraceID: {trace_id}")

        status_code_holder: dict[str, Optional[int]] = {"status": None}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_code_holder["status"] = int(message["status"])

                if self.attach_response_header:
                    headers = list(message.get("headers", []))
                    headers.append((self.response_header_name.lower().encode(), trace_id.encode()))
                    message["headers"] = headers
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            status = status_code_holder["status"]
            status_part = f"{status}" if status is not None else "unknown"
            self.logger.debug(
                f"Request finished: {request.method} {request.url} - TraceID: {trace_id} - Status: {status_part}"
            )
            trace_id_var.reset(token)
