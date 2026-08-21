from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.organization import OrganizationUnit


router = APIRouter(
    prefix="/organization-tree",
    tags=["Organization Tree"]
)


@router.get("")
def get_organization_tree(
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


    def build_tree(unit):

        return {
            "id": unit.id,
            "name": unit.name,
            "code": unit.code,
            "type": unit.unit_type,

            "children": [
                build_tree(child)
                for child in unit.children
                if child.is_active
            ]
        }


    return [
        build_tree(root)
        for root in roots
    ]