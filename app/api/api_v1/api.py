from fastapi import APIRouter
from app.api.api_v1 import endpoints
from app.api.api_v1.endpoints import login, administrators, roles, endpoints, endpoint_roles

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(administrators.router, prefix="/administrators", tags=["administrators"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(endpoints.router, prefix="/endpoints", tags=["endpoints"])
api_router.include_router(endpoint_roles.router, prefix="/endpoint-roles", tags=["endpoint-roles"])