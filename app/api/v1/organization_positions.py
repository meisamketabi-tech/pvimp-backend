from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.db.models.organization_unit_position import OrganizationUnitPosition
from app.schemas.organization_unit_position import (
    OrganizationUnitPositionCreate,
    OrganizationUnitPositionRead,
)


router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)


@router.post(
    "/positions",
    response_model=OrganizationUnitPositionRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_position(
    payload: OrganizationUnitPositionCreate,
    db: Session = Depends(get_db),
):

    exists = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id
            == payload.organization_unit_id,
            OrganizationUnitPosition.organization_position_id
            == payload.organization_position_id,
            OrganizationUnitPosition.is_active == True,
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Position already exists for this unit",
        )

    obj = OrganizationUnitPosition(
        organization_unit_id=payload.organization_unit_id,
        organization_position_id=payload.organization_position_id,
        parent_assignment_id=payload.parent_assignment_id,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj



@router.get(
    "/{unit_id}/positions",
    response_model=list[OrganizationUnitPositionRead],
)
def get_unit_positions(
    unit_id: int,
    db: Session = Depends(get_db),
):

    return (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit_id,
            OrganizationUnitPosition.is_active == True,
        )
        .order_by(
            OrganizationUnitPosition.id.asc()
        )
        .all()
    )



@router.delete(
    "/positions/{position_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("admin"))],
)
def disable_position(
    position_id: int,
    db: Session = Depends(get_db),
):

    obj = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.id == position_id
        )
        .first()
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )

    for assignment in obj.assignments:
        assignment.is_active = False

    obj.is_active = False

    db.commit()

    return None
