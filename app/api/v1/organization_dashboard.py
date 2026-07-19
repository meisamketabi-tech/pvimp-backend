from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition


router = APIRouter(
    prefix="/organization",
    tags=["Organization Dashboard"],
)


@router.get("/dashboard")
def organization_dashboard(
    db: Session = Depends(get_db),
):

    total_units = (
        db.query(func.count(OrganizationUnit.id))
        .filter(
            OrganizationUnit.is_active == True
        )
        .scalar()
    )


    total_users = (
        db.query(
            func.count(
                func.distinct(
                    UserAssignment.user_id
                )
            )
        )
        .filter(
            UserAssignment.is_active == True
        )
        .scalar()
    )


    total_positions = (
        db.query(func.count(OrganizationUnitPosition.id))
        .filter(
            OrganizationUnitPosition.is_active == True
        )
        .scalar()
    )


    filled_positions = (
        db.query(
            func.count(
                func.distinct(
                    UserAssignment.organization_unit_position_id
                )
            )
        )
        .filter(
            UserAssignment.is_active == True,
            UserAssignment.organization_unit_position_id != None,
        )
        .scalar()
    )


    return {
        "total_units": total_units,
        "total_users": total_users,
        "total_positions": total_positions,
        "filled_positions": filled_positions,
        "empty_positions": total_positions - filled_positions,
    }
