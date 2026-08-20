from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token, UserMe


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    token = create_access_token(data={"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
    }


@router.get(
    "/me",
    response_model=UserMe,
)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assignments = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.user_id == current_user.id,
            UserAssignment.is_active.is_(True),
        )
        .all()
    )
    roles = [
        assignment.role.name.strip()
        for assignment in assignments
        if assignment.role is not None and assignment.role.name
    ]

    return UserMe(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        email=current_user.email,
        mobile=current_user.mobile,
        is_active=current_user.is_active,
        role=roles[0] if roles else None,
        roles=roles,
    )
