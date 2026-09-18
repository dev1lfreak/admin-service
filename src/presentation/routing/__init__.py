from fastapi import APIRouter

from src.presentation.routing.auth import auth_router
from src.presentation.routing.documents import documents_router
from src.presentation.routing.jwt import jwt_router
from src.presentation.routing.organizations import organizations_router
from src.presentation.routing.purchase_requests import purchase_requests_router
from src.presentation.routing.users import users_router
from src.presentation.routing.search import search_router
from src.presentation.routing.orders import orders_router
from src.presentation.routing.analytics import analytics_router

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(auth_router)
v1_router.include_router(jwt_router)
v1_router.include_router(organizations_router)
v1_router.include_router(documents_router)
v1_router.include_router(purchase_requests_router)
v1_router.include_router(users_router)
v1_router.include_router(search_router)
v1_router.include_router(orders_router)
v1_router.include_router(analytics_router)