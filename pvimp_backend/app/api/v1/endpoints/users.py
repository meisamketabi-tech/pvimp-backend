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
    UserRoleCreate,
    UserRoleRead,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> UserRead:
    service = UserService(db)
    try:
        return service.create_user(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=List[UserRead],
)
def list_users(
    db: Session = Depends(get_db),
) -> List[UserRead]:
    service = UserService(db)
    return service.list_users()


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserRead:
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserRead,
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> UserRead:
    service = UserService(db)
    user = service.update_user(user_id, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post(
    "/roles",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
) -> RoleRead:
    service = UserService(db)
    return service.create_role(payload)


@router.get(
    "/roles",
    response_model=List[RoleRead],
    dependencies=[Depends(require_roles("admin"))],
)
def list_roles(
    db: Session = Depends(get_db),
) -> List[RoleRead]:
    service = UserService(db)
    return service.list_roles()


@router.get(
    "/roles/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(require_roles("admin"))],
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
) -> RoleRead:
    service = UserService(db)
    role = service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
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
) -> RoleRead:
    service = UserService(db)
    role = service.update_role(role_id, payload)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return role


@router.post(
    "/roles/assign",
    response_model=UserRoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def assign_role(
    payload: UserRoleCreate,
    db: Session = Depends(get_db),
) -> UserRoleRead:
    service = UserService(db)
    return service.assign_role(payload)


@router.get(
    "/{user_id}/roles",
    response_model=List[UserRoleRead],
    dependencies=[Depends(require_roles("admin"))],
)
def list_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
) -> List[UserRoleRead]:
    service = UserService(db)
    return service.list_user_roles(user_id)
