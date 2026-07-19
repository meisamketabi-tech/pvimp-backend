from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.permissions import require_permission

from app.db.session import get_db

from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition


router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)



@router.get("/tree")
def organization_tree(
    db: Session = Depends(get_db),
    user=Depends(
        require_permission("VIEW_ORGANIZATION")
    ),
):

    from app.services.organization_service import build_tree

    return build_tree(db)



@router.get("/dashboard")
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



@router.get("/{unit_id}")
def organization_detail(
    unit_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_permission("VIEW_ORGANIZATION")
    ),
):

    unit = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.id == unit_id
        )
        .first()
    )


    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Organization unit not found",
        )


    positions = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit.id,
            OrganizationUnitPosition.is_active == True,
        )
        .all()
    )


    users = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.organization_unit_id == unit.id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    return {

        "id": unit.id,

        "name": unit.name,

        "code": unit.code,

        "type_id": unit.type_id,

        "level_id": unit.level_id,


        "positions": [

            {
                "id": p.organization_position.id,
                "title": p.organization_position.title,
            }

            for p in positions

        ],


        "users": [

            {
                "id": u.user.id,
                "username": u.user.username,
                "full_name": u.user.full_name,
                "role_id": u.role.id,
                "role": u.role.name,
                "is_primary": u.is_primary,
            }

            for u in users

        ],

    }



@router.get("/{unit_id}/users")
def organization_users(
    unit_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_permission("VIEW_USERS")
    ),
):

    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.organization_unit_id == unit_id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    return [

        {
            "user_id": a.user.id,
            "username": a.user.username,
            "full_name": a.user.full_name,
            "role_id": a.role.id,
            "role_name": a.role.name,
            "is_primary": a.is_primary,
        }

        for a in assignments

    ]



@router.get("/{unit_id}/positions")
def organization_positions(
    unit_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_permission("VIEW_ASSIGNMENTS")
    ),
):

    positions = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit_id,
            OrganizationUnitPosition.is_active == True,
        )
        .all()
    )


    return [

        {
            "assignment_id": p.id,
            "position_id": p.organization_position.id,
            "position_title": p.organization_position.title,
        }

        for p in positions

    ]