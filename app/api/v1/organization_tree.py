from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_unit_position import OrganizationUnitPosition

from app.schemas.organization_tree import OrganizationTreeNode

router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)


def build_tree(unit, db):

    unit_positions = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit.id,
            OrganizationUnitPosition.is_active == True,
        )
        .all()
    )

    positions = []

    for item in unit_positions:

        if item.organization_position:

            positions.append(
                {
                    "id": item.id,
                    "position_id": item.organization_position.id,
                    "position_code": item.organization_position.code,
                    "position_title": item.organization_position.title,
                    "assigned_users": len(item.assignments),
                }
            )

    return {
        "id": unit.id,
        "name": unit.name,
        "code": unit.code,
        "unit_type": unit.unit_type,
        "parent_id": unit.parent_id,
        "positions": positions,
        "position_count": len(positions),
        "children": [
            build_tree(child, db) for child in unit.children if child.is_active
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

    return [build_tree(root, db) for root in roots]
