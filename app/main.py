from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.organization_crud import router as organization_crud_router
from app.api.routes.organization_tree import router as organization_tree_router
from app.api.routes.position import router as position_router
from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    default_response_class=JSONResponse,
)


# The frontend is currently served by Vite on localhost:5173.
# 127.0.0.1:5173 is also allowed because browsers treat it as a
# different origin from localhost:5173.
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")

app.include_router(organization_crud_router)
app.include_router(position_router)
app.include_router(organization_tree_router)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}
