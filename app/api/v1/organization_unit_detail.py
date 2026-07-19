from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition


router = APIRouter(
    prefix="/organization",
    tags=["Organization Detail"],
)


@router.get("/unit/{unit_id}/detail")
def organization_unit_detail(
    unit_id: int,
    db: Session = Depends(get_db),
):

    unit = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.id == unit_id,
            OrganizationUnit.is_active == True,
        )
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found",
        )


    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.organization_unit_id == unit_id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    positions = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit_id,
            OrganizationUnitPosition.is_active == True,
        )
        .all()
    )


    return {

        "id": unit.id,
        "name": unit.name,
        "code": unit.code,
        "unit_type": unit.unit_type,
        "parent_id": unit.parent_id,


        "users": [
            {
                "assignment_id": a.id,
                "user_id": a.user.id,
                "username": a.user.username,
                "full_name": a.user.full_name,
                "role": a.role.name,
                "position_id": (
                    a.organization_unit_position.id
                    if a.organization_unit_position
                    else None
                ),
            }
            for a in assignments
        ],


        "positions": [
            {
                "id": p.id,
                "position_id": p.organization_position.id,
                "position_code": p.organization_position.code,
                "position_title": p.organization_position.title,
                "assigned_users": len(
                    p.assignments
                ),
            }
            for p in positions
        ],


        "children": [
            {
                "id": c.id,
                "name": c.name,
                "unit_type": c.unit_type,
            }
            for c in unit.children
            if c.is_active
        ],
    }
