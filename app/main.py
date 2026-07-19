from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

from app.api.routes.organization import router as organization_router
from app.api.routes.organization_crud import router as organization_crud_router
from app.api.routes.position import router as position_router


app = FastAPI(
    title=settings.APP_NAME
)


app.include_router(
    api_router,
    prefix="/api/v1"
)


app.include_router(
    organization_router
)


app.include_router(
    organization_crud_router
)

app.include_router(
    position_router
)


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running"
    }