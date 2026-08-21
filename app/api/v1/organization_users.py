from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.assignment import UserAssignment
from app.db.models.organization import OrganizationUnit


router = APIRouter(
    prefix="/organization",
    tags=["Organization Users"]
)


@router.get("/{organization_id}/users")
def get_organization_users(
    organization_id: int,
    db: Session = Depends(get_db),
):

    unit = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.id == organization_id
        )
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found"
        )


    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.organization_unit_id == organization_id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    result = []

    for item in assignments:

        result.append(
            {
                "user_id": item.user.id,
                "username": item.user.username,
                "full_name": item.user.full_name,
                "role_id": item.role.id,
                "role_name": item.role.name,
            }
        )


    return result