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

    return {

        "organization_units":
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.is_active == True
            )
            .count(),

        "active_assignments":
            db.query(UserAssignment)
            .filter(
                UserAssignment.is_active == True
            )
            .count(),

        "defined_positions":
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.is_active == True
            )
            .count(),

        "managers":
            db.query(UserAssignment)
            .filter(
                UserAssignment.is_active == True,
                UserAssignment.is_primary == True,
            )
            .count(),

    }



@router.get("/{unit_id}")
def organization_detail(
    unit_id: int,
    db: Session = Depends(get_db),
):

    from app.db.models.organization_responsibility import OrganizationResponsibility


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


    responsibilities = (
        db.query(OrganizationResponsibility)
        .filter(
            OrganizationResponsibility.organization_unit_id == unit.id
        )
        .all()
    )


    children = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.parent_id == unit.id,
            OrganizationUnit.is_active == True,
        )
        .all()
    )


    return {

        "id": unit.id,
        "name": unit.name,
        "code": unit.code,
        "unit_type": unit.unit_type,
        "parent_id": unit.parent_id,


        "positions": [

            {
                "id": p.id,
                "position_id": p.organization_position.id,
                "position_code": p.organization_position.code,
                "position_title": p.organization_position.title,
                "assigned_users": 0,
            }

            for p in positions

        ],


        "users": [

            {
                "assignment_id": u.id,
                "user_id": u.user.id,
                "full_name": u.user.full_name,
                "role": u.role.name,
            }

            for u in users

        ],


        "responsibilities": [

            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "priority": r.priority,
                "inspection_type_id": r.inspection_type_id,
                "inspection_type":
                    r.inspection_type.title
                    if r.inspection_type
                    else None,
            }

            for r in responsibilities

        ],


        "children": [

            {
                "id": c.id,
                "name": c.name,
                "unit_type": c.unit_type,
            }

            for c in children

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