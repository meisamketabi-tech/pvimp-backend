
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_vaccine_distribution import (
    GISVaccineDistribution
)

from app.schemas.gis.vaccine_distribution import (
    VaccineDistributionCreate,
    VaccineDistributionResponse
)


router = APIRouter(
    prefix="/gis/vaccine-distributions",
    tags=["GIS Vaccine Distribution"]
)


@router.get(
    "/",
    response_model=list[VaccineDistributionResponse]
)
def list_items(
    db: Session = Depends(get_db)
):

    return db.query(
        GISVaccineDistribution
    ).all()



@router.post(
    "/",
    response_model=VaccineDistributionResponse
)
def create_item(
    data: VaccineDistributionCreate,
    db: Session = Depends(get_db)
):

    item = GISVaccineDistribution(
        **data.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
