from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db

from app.db.models.user import User
from app.db.models.assignment import UserAssignment
from app.db.models.permission import Permission
from app.db.models.role_permission import RolePermission



def has_permission(
    db: Session,
    user: User,
    permission_code: str,
) -> bool:

    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.user_id == user.id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    if not assignments:
        return False


    role_ids = [
        assignment.role_id
        for assignment in assignments
    ]


    permission = (
        db.query(Permission)
        .filter(
            Permission.code == permission_code,
            Permission.is_active == True,
        )
        .first()
    )


    if not permission:
        return False


    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id.in_(role_ids),
            RolePermission.permission_id == permission.id,
            RolePermission.is_active == True,
        )
        .first()
    )


    return role_permission is not None



def require_permission(permission_code: str):

    def checker(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):

        if not has_permission(
            db,
            user,
            permission_code,
        ):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )


        return user


    return checker