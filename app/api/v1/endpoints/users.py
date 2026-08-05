from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles, get_current_user

from app.schemas.user import (
    RoleCreate,
    RoleRead,
    RoleUpdate,
    UserCreate,
    UserRead,
    AssignmentCreate,
    AssignmentRead,
    UserUpdate,
)

from app.services.user_service import UserService
from app.db.models.user import User
from app.db.models.assignment import UserAssignment

router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService(db).create_user(payload)


@router.get(
    "/{user_id}/details",
)
def user_details(
    user_id: int,
    db: Session = Depends(get_db),
):

    from sqlalchemy.orm import joinedload

    user = (
        db.query(User)
        .options(
            joinedload(User.assignments).joinedload(UserAssignment.organization_unit),
            joinedload(User.assignments).joinedload(UserAssignment.role),
            joinedload(User.assignments).joinedload(
                UserAssignment.organization_unit_position
            ),
        )
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "mobile": user.mobile,
        "is_active": user.is_active,
        "assignments": [
            {
                "id": a.id,
                "organization_unit": (
                    {
                        "id": a.organization_unit.id,
                        "name": a.organization_unit.name,
                        "code": a.organization_unit.code,
                    }
                    if a.organization_unit
                    else None
                ),
                "position": (
                    {
                        "id": a.organization_unit_position.id,
                    }
                    if a.organization_unit_position
                    else None
                ),
                "role": (
                    {
                        "id": a.role.id,
                        "name": a.role.name,
                    }
                    if a.role
                    else None
                ),
                "is_primary": a.is_primary,
                "is_active": a.is_active,
                "start_date": a.start_date,
                "end_date": a.end_date,
            }
            for a in user.assignments
            if a.is_active
        ],
    }
