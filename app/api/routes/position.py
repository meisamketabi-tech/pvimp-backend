
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.position_service import PositionService
from app.db.models.organization_position import OrganizationPosition


router = APIRouter(
    prefix="/positions",
    tags=["Positions"],
)


@router.get("")
def list_positions(
    db: Session = Depends(get_db),
):
    return PositionService().list_positions(db)



@router.post("")
def create_position(
    payload: dict,
    db: Session = Depends(get_db),
):
    return PositionService().create_position(
        db,
        payload["title"],
        payload["code"],
    )



@router.post("/assign")
def assign_position(
    payload: dict,
    db: Session = Depends(get_db),
):

    return PositionService().assign_position(
        db,
        payload["organization_unit_id"],
        payload["position_id"],
    )



@router.get("/unit/{unit_id}")
def unit_positions(
    unit_id: int,
    db: Session = Depends(get_db),
):

    return PositionService().list_unit_positions(
        db,
        unit_id,
    )
