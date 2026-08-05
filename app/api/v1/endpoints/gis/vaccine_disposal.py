from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_vaccine_disposal import (
    GISVaccineDisposal
)

from app.schemas.gis.vaccine_disposal import (
    VaccineDisposalCreate,
    VaccineDisposalResponse
)


router = APIRouter(
    prefix="/gis/vaccine-disposals",
    tags=["GIS Vaccine Disposal"]
)


@router.get(
    "/",
    response_model=list[VaccineDisposalResponse]
)
def list_items(
    db: Session = Depends(get_db)
):

    return db.query(
        GISVaccineDisposal
    ).all()



@router.post(
    "/",
    response_model=VaccineDisposalResponse
)
def create_item(
    data: VaccineDisposalCreate,
    db: Session = Depends(get_db)
):

    item = GISVaccineDisposal(
        **data.model_dump()
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item