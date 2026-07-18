from fastapi import APIRouter

from app.api.v1.endpoints import (
    inspection,
    health,
    inspection_assignment,
)


api_router = APIRouter()


api_router.include_router(
    health.router
)


api_router.include_router(
    inspection.router
)


api_router.include_router(
    inspection_assignment.router
)