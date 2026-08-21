from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.models.assignment import UserAssignment
from app.db.models.organization import OrganizationUnit
from app.db.models.role import Role
from app.db.models.user import User
from app.db.session import SessionLocal
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


# =========================================================
# Database
# =========================================================


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# Current user
# =========================================================


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        username = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenData(
            username=username,
        )

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(
            User.username == token_data.username,
            User.is_active.is_(True),
        )
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


# =========================================================
# Active assignments
# =========================================================


def get_active_assignments(
    db: Session,
    user: User,
) -> list[UserAssignment]:
    return (
        db.query(UserAssignment)
        .join(
            Role,
            Role.id == UserAssignment.role_id,
        )
        .join(
            OrganizationUnit,
            OrganizationUnit.id == UserAssignment.organization_unit_id,
        )
        .filter(
            UserAssignment.user_id == user.id,
            UserAssignment.is_active.is_(True),
            Role.is_active.is_(True),
            OrganizationUnit.is_active.is_(True),
        )
        .all()
    )


# =========================================================
# Role helpers
# =========================================================

GLOBAL_SCOPE_ROLES = {
    "admin",
    "director_general",
    "health_deputy",
    "مدیرکل دامپزشکی استان",
}

COUNTY_SCOPE_ROLES = {
    "county_head",
    "رئیس اداره",
}


def _get_role_names(
    assignments: list[UserAssignment],
) -> set[str]:
    return {
        assignment.role.name.strip().lower()
        for assignment in assignments
        if assignment.role is not None and assignment.role.name
    }


# =========================================================
# Role guard
# =========================================================


def require_roles(*allowed_roles: str):
    normalized_allowed = {
        role.strip().lower() for role in allowed_roles if role and role.strip()
    }

    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:

        if not normalized_allowed:
            return current_user

        assignments = get_active_assignments(
            db,
            current_user,
        )

        user_roles = _get_role_names(assignments)

        if not user_roles.intersection(normalized_allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role permission denied",
            )

        return current_user

    return dependency


# =========================================================
# Permission / scope
# =========================================================


def is_global_scope_user(
    db: Session,
    user: User,
) -> bool:
    assignments = get_active_assignments(
        db,
        user,
    )

    role_names = _get_role_names(assignments)

    return bool(
        role_names.intersection({role.strip().lower() for role in GLOBAL_SCOPE_ROLES})
    )


def get_allowed_county_ids(
    db: Session,
    user: User,
) -> set[int] | None:
    assignments = get_active_assignments(
        db,
        user,
    )

    if not assignments:
        return set()

    role_names = _get_role_names(assignments)

    # Global users can access all counties.
    if role_names.intersection({role.strip().lower() for role in GLOBAL_SCOPE_ROLES}):
        return None

    county_ids: set[int] = set()

    normalized_county_roles = {role.strip().lower() for role in COUNTY_SCOPE_ROLES}

    for assignment in assignments:
        role = assignment.role

        if role is None or not role.name:
            continue

        role_name = role.name.strip().lower()

        if role_name not in normalized_county_roles:
            continue

        organization_unit = assignment.organization_unit

        if organization_unit is None:
            continue

        if organization_unit.county_id is not None:
            county_ids.add(int(organization_unit.county_id))

    return county_ids


# =========================================================
# Token creation
# =========================================================


def create_token_for_user(
    user: User,
) -> str:
    return create_access_token(
        data={
            "sub": user.username,
        },
    )
