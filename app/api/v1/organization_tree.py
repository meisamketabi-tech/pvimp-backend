from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.schemas.organization_tree import OrganizationTreeNode


router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)


def build_tree(unit):

    assignments = (
        unit.assignments
        if hasattr(unit, "assignments")
        else []
    )

    positions = []

    for assignment in assignments:

        if not assignment.is_active:
            continue

        if not assignment.organization_unit_position:
            continue

        position = assignment.organization_unit_position.organization_position

        user = assignment.user

        item = {
            "id": assignment.organization_unit_position.id,

            "position_id": position.id,
            "position_code": position.code,
            "position_title": position.title,

            "user_id": user.id if user else None,
            "username": user.username if user else None,
            "full_name": user.full_name if user else None,
        }

        if item not in positions:
            positions.append(item)


    return {
        "id": unit.id,
        "name": unit.name,
        "code": unit.code,
        "unit_type": unit.unit_type,
        "parent_id": unit.parent_id,

        "positions": positions,

        "children": [
            build_tree(child)
            for child in unit.children
            if child.is_active
        ],
    }



@router.get(
    "/tree",
    response_model=list[OrganizationTreeNode],
)
def organization_tree(
    db: Session = Depends(get_db),
):

    roots = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.parent_id == None,
            OrganizationUnit.is_active == True,
        )
        .all()
    )

    return [
        build_tree(root)
        for root in roots
    ]
