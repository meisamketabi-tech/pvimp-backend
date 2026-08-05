
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.gis_laboratory_result import GISLaboratoryResult
from app.schemas.gis.laboratory_result import (
    LaboratoryResultCreate,
    LaboratoryResultResponse,
)


router = APIRouter(
    prefix="/gis/laboratory-results",
    tags=["GIS Laboratory Results"],
)


@router.get("/", response_model=list[LaboratoryResultResponse])
def list_results(
    db: Session = Depends(get_db),
):
    return db.query(GISLaboratoryResult).all()


@router.post("/", response_model=LaboratoryResultResponse)
def create_result(
    data: LaboratoryResultCreate,
    db: Session = Depends(get_db),
):

    item = GISLaboratoryResult(
        **data.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
