from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_vaccine_inventory import (
    GISVaccineInventory
)

from app.schemas.gis.vaccine_inventory import (
    VaccineInventoryCreate,
    VaccineInventoryResponse
)


router = APIRouter(
    prefix="/gis/vaccine-inventories",
    tags=["GIS Vaccine Inventory"]
)



@router.get(
    "/",
    response_model=list[VaccineInventoryResponse]
)
def list_items(
    db: Session = Depends(get_db)
):

    return db.query(
        GISVaccineInventory
    ).all()



@router.post(
    "/",
    response_model=VaccineInventoryResponse
)
def create_item(
    data: VaccineInventoryCreate,
    db: Session = Depends(get_db)
):

    item = GISVaccineInventory(
        **data.model_dump()
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item