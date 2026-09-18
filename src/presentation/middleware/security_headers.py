from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        hsts: bool = True,
        hsts_max_age: int = 31536000,  # 1 год
        hsts_include_subdomains: bool = True,
        hsts_preload: bool = False,
        frame_options: str = 'DENY',  # или 'SAMEORIGIN'
        referrer_policy: str = 'strict-origin-when-cross-origin',
        content_security_policy: str | None = None,
    ):
        super().__init__(app)
        self.hsts = hsts
        self.hsts_max_age = hsts_max_age
        self.hsts_include_subdomains = hsts_include_subdomains
        self.hsts_preload = hsts_preload
        self.frame_options = frame_options
        self.referrer_policy = referrer_policy
        self.csp = content_security_policy

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        if request.url.path in ('/docs', '/redoc', '/openapi.json'):
            return response

        if self.hsts and request.url.scheme == 'https':
            hsts = f'max-age={self.hsts_max_age}'
            if self.hsts_include_subdomains:
                hsts += '; includeSubDomains'
            if self.hsts_preload:
                hsts += '; preload'
            response.headers['Strict-Transport-Security'] = hsts

        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        response.headers['X-Frame-Options'] = self.frame_options

        response.headers['Referrer-Policy'] = self.referrer_policy

        if self.csp:
            response.headers['Content-Security-Policy'] = self.csp

        return response
