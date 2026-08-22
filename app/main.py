from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from app.api.routes.organization_tree import router as organization_tree_router
from app.core.config import settings
from app.api.v1.router import api_router

from app.api.routes.organization_crud import router as organization_crud_router
from app.api.routes.position import router as position_router

from app.api.v1.endpoints.gis import vaccination_kpi
from app.db.session import SessionLocal
from app.services.gis.vaccination_kpi_view import ensure_vaccination_kpi_view
from app.services.gis import vaccination_kpi_service

app = FastAPI(title=settings.APP_NAME, default_response_class=JSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def initialize_vaccination_kpi_semantic_layer():
    db = SessionLocal()
    try:
        ensure_vaccination_kpi_view(db)
    finally:
        db.close()

    # Keep all existing KPI service functions/routes intact while switching
    # their source transparently to the normalized semantic view.
    vaccination_kpi_service.VACCINATION_TABLE = (
        "(SELECT * FROM gis_vaccination_kpi "
        "WHERE activity_type = 'VACCINATION') AS vaccination_kpi"
    )


app.include_router(api_router, prefix="/api/v1")

app.include_router(organization_crud_router)
app.include_router(position_router)
app.include_router(organization_tree_router)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}
