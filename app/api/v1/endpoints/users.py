from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
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
    service = UserService(db)
    return service.create_user(payload)


@router.get(
    "",
    response_model=List[UserRead],
)
def list_users(
    db: Session = Depends(get_db),
):
    return UserService(db).list_users()


@router.get(
    "/roles",
    response_model=List[RoleRead],
    dependencies=[Depends(require_roles("admin"))],
)
def list_roles(
    db: Session = Depends(get_db),
):
    return UserService(db).list_roles()


@router.post(
    "/roles",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
):
    return UserService(db).create_role(payload)


@router.get(
    "/roles/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(require_roles("admin"))],
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    role = UserService(db).get_role(role_id)
    if not role:
        raise HTTPException(404, "Role not found")
    return role


@router.put(
    "/roles/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(require_roles("admin"))],
)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
):
    role = UserService(db).update_role(role_id, payload)
    if not role:
        raise HTTPException(404, "Role not found")
    return role


@router.post(
    "/assignments",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
):
    return UserService(db).assign_role(payload)


@router.get(
    "/{user_id}/assignments",
    response_model=List[AssignmentRead],
    dependencies=[Depends(require_roles("admin"))],
)
def list_assignments(
    user_id: int,
    db: Session = Depends(get_db),
):
    return UserService(db).list_user_roles(user_id)


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = UserService(db).get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put(
    "/{user_id}",
    response_model=UserRead,
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    user = UserService(db).update_user(user_id, payload)
    if not user:
        raise HTTPException(404, "User not found")
    return user




@router.get(
    "/{user_id}/details",
)
def user_details(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.user_id == user_id,
            UserAssignment.is_active == True,
        )
        .all()
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

                "organization_unit": {
                    "id": a.organization_unit.id,
                    "name": a.organization_unit.name,
                    "code": a.organization_unit.code,
                },

                "position": (
                    {
                        "id": a.organization_unit_position.organization_position.id,
                        "code": a.organization_unit_position.organization_position.code,
                        "title": a.organization_unit_position.organization_position.title,
                    }
                    if a.organization_unit_position
                    else None
                ),

                "role": {
                    "id": a.role.id,
                    "name": a.role.name,
                },

                "is_primary": a.is_primary,
                "start_date": a.start_date,
                "end_date": a.end_date,
            }
            for a in assignments
        ],
    }
