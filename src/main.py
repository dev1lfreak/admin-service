from __future__ import annotations

from contextlib import asynccontextmanager
import secrets
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, status
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.cors import CORSMiddleware

from src.application.domain.exceptions import ApplicationException
from src.infrastructure.config.settings import get_settings
from src.infrastructure.crypto.wallet_crypto import load_master_key
from src.infrastructure.security.key_store import JwtKeyStore
from src.infrastructure.utils import generate_instance_id
from src.infrastructure.logger import logger
from src.infrastructure.config import settings
from src.presentation.handler import application_exception_handler
from src.presentation.handler import unhandled_exception_handler
from src.presentation.middleware import TraceIDMiddleware, SecurityHeadersMiddleware
from src.presentation.routing import v1_router
from src.presentation.schemas import ErrorResponse

security = HTTPBasic()

ERROR_RESPONSES: dict[int, str] = {
    status.HTTP_400_BAD_REQUEST: 'Bad Request',
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
    status.HTTP_403_FORBIDDEN: 'Forbidden',
    status.HTTP_404_NOT_FOUND: 'Not Found',
    status.HTTP_409_CONFLICT: 'Conflict',
    status.HTTP_429_TOO_MANY_REQUESTS: 'Too Many Requests',
    status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal Server Error',
    status.HTTP_503_SERVICE_UNAVAILABLE: 'Service Unavailable',
}


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        license_info=app.license_info,
    )
    components = openapi_schema.setdefault('components', {})
    schemas = components.setdefault('schemas', {})
    schemas['ErrorResponse'] = ErrorResponse.model_json_schema()

    for path_item in openapi_schema.get('paths', {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            responses = operation.setdefault('responses', {})
            for status_code, description in ERROR_RESPONSES.items():
                responses.setdefault(
                    str(status_code),
                    {
                        'description': description,
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/ErrorResponse'},
                            },
                        },
                    },
                )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


async def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> HTTPBasicCredentials:
    user_ok = secrets.compare_digest(credentials.username, settings.DOCS_USERNAME)
    pass_ok = secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)
    if not (user_ok and pass_ok):
        raise ApplicationException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message='Unauthorized',
            headers={'WWW-Authenticate': 'Basic'},
        )
    return credentials


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    instance_id = generate_instance_id()
    logger.set_instance_id(instance_id)
    logger.info(f'Admin service instance started with id {instance_id}')

    jwt_store = JwtKeyStore(
        active_kid=settings.JWT_ACTIVE_KID,
        private_key=settings.JWT_PRIVATE_KEY,
        public_key=settings.JWT_PUBLIC_KEY,
        previous_kid=settings.JWT_PREVIOUS_KID,
        previous_public_key=settings.JWT_PREVIOUS_PUBLIC_KEY,
    )
    app.state.jwt_key_store = jwt_store

    load_master_key(settings.CRYPTO_MASTER_KEY)
    logger.info('Crypto master key loaded')
    yield
    logger.info('Shutting down...')
    logger.info('Admin service stopped')


app: FastAPI = FastAPI(
    redoc_url=None,
    docs_url=None,
    lifespan=lifespan,
    title='Elcsa. Admin Service',
    version='1.0.0',
    description='Admin API for legal entities, wallets, documents, and B2B purchase requests',
    license_info={'name': 'MIT', 'url': 'https://opensource.org/licenses/MIT'},
)

app.add_exception_handler(ApplicationException, application_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.include_router(v1_router)

app.add_middleware(TraceIDMiddleware, logger=logger)
app.add_middleware(
    SecurityHeadersMiddleware,
    hsts=True,
    hsts_preload=False,
    frame_options='DENY',
    referrer_policy='strict-origin-when-cross-origin',
    content_security_policy="default-src 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'",
)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - Swagger UI',
        oauth2_redirect_url=getattr(app, 'swagger_ui_oauth2_redirect_url', None),
        swagger_js_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js',
        swagger_css_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui.css',
    )


@app.get('/redoc', include_in_schema=False)
async def custom_redoc_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)) -> HTMLResponse:
    return get_redoc_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - ReDoc',
        redoc_js_url='https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
    )


@app.post('/ping')
async def ping() -> dict[str, str]:
    return {'message': 'pong', 'status': 'ok'}

@app.get('/health')
async def health() -> dict[str, str]:
    return {
        'status': 'ok',
    }

app.openapi = custom_openapi
