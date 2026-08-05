
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.gis_vaccination_performance import GISVaccinationPerformance
from app.schemas.gis.vaccination_performance import (
    VaccinationPerformanceCreate,
    VaccinationPerformanceResponse
)


router = APIRouter(
    prefix="/gis/vaccination-performances",
    tags=["GIS Vaccination Performance"]
)


@router.get("/", response_model=list[VaccinationPerformanceResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(GISVaccinationPerformance).all()


@router.post("/", response_model=VaccinationPerformanceResponse)
def create_item(
    data: VaccinationPerformanceCreate,
    db: Session = Depends(get_db)
):

    item = GISVaccinationPerformance(
        **data.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
