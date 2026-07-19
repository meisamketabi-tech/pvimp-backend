from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.permissions import require_permission

from app.db.session import get_db

from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition


router = APIRouter(
    prefix="/organization/dashboard",
    tags=["Organization Dashboard"],
)



@router.get("/")
def organization_dashboard(
    db: Session = Depends(get_db),
    user=Depends(
        require_permission("VIEW_DASHBOARD")
    ),
):

    units_count = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.is_active == True
        )
        .count()
    )


    users_count = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.is_active == True
        )
        .count()
    )


    positions_count = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.is_active == True
        )
        .count()
    )


    managers_count = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.is_active == True,
            UserAssignment.is_primary == True,
        )
        .count()
    )


    return {

        "organization_units": units_count,

        "active_assignments": users_count,

        "defined_positions": positions_count,

        "managers": managers_count,

    }