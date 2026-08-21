
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.gis_disease_report import GISDiseaseReport
from app.schemas.gis.disease_report import (
    DiseaseReportCreate,
    DiseaseReportResponse
)


router = APIRouter(
    prefix="/gis/disease-reports",
    tags=["GIS Disease Reports"]
)


@router.get("/", response_model=list[DiseaseReportResponse])
def list_reports(
    db: Session = Depends(get_db)
):
    return db.query(GISDiseaseReport).all()


@router.post("/", response_model=DiseaseReportResponse)
def create_report(
    data: DiseaseReportCreate,
    db: Session = Depends(get_db)
):

    item = GISDiseaseReport(
        **data.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
