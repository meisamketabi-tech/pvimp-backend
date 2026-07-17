app/api/deps.py
from typing import Generator, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import SessionLocal
from app.db.models.user import User
from app.schemas.auth import TokenData


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.username == token_data.username)
        .first()
    )
    if not user or not user.is_active:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: str):
    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_roles = current_user.roles or []
        role_names: List[str] = [
            user_role.role.name
            for user_role in user_roles
            if user_role.role is not None
        ]

        if not any(role in role_names for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency


def create_token_for_user(user: User) -> str:
    data = {"sub": user.username}
    return create_access_token(data=data)
