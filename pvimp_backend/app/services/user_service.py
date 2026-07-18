from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.assignment import UserAssignment
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


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _ensure_unique_user_fields(
        self,
        username: str,
        email: Optional[str],
        mobile: Optional[str],
        user_id: Optional[int] = None,
    ) -> None:
        query = self.db.query(User)

        if user_id is not None:
            query = query.filter(User.id != user_id)

        if username:
            existing = query.filter(User.username == username).first()
            if existing:
                raise ValueError("Username already exists")

        if email:
            existing = query.filter(User.email == email).first()
            if existing:
                raise ValueError("Email already exists")

        if mobile:
            existing = query.filter(User.mobile == mobile).first()
            if existing:
                raise ValueError("Mobile already exists")

    def create_user(self, user_in: UserCreate) -> UserRead:
        self._ensure_unique_user_fields(
            username=user_in.username,
            email=user_in.email,
            mobile=user_in.mobile,
        )

        password_hash = get_password_hash(user_in.password)

        db_user = User(
            username=user_in.username,
            full_name=user_in.full_name,
            email=user_in.email,
            mobile=user_in.mobile,
            default_veterinary_unit_id=user_in.default_veterinary_unit_id,
            is_active=user_in.is_active,
            password_hash=password_hash,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return UserRead.model_validate(db_user)

    def list_users(self) -> List[UserRead]:
        users = (
            self.db.query(User)
            .order_by(User.id.asc())
            .all()
        )
        return [UserRead.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> Optional[UserRead]:
        user = self.db.query(User).get(user_id)
        if not user:
            return None
        return UserRead.model_validate(user)

    def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[UserRead]:
        db_user = self.db.query(User).get(user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)

        if "username" in update_data:
            self._ensure_unique_user_fields(
                username=update_data["username"],
                email=update_data.get("email", db_user.email),
                mobile=update_data.get("mobile", db_user.mobile),
                user_id=db_user.id,
            )
            db_user.username = update_data["username"]

        if "email" in update_data:
            self._ensure_unique_user_fields(
                username=db_user.username,
                email=update_data["email"],
                mobile=update_data.get("mobile", db_user.mobile),
                user_id=db_user.id,
            )
            db_user.email = update_data["email"]

        if "mobile" in update_data:
            self._ensure_unique_user_fields(
                username=db_user.username,
                email=update_data.get("email", db_user.email),
                mobile=update_data["mobile"],
                user_id=db_user.id,
            )
            db_user.mobile = update_data["mobile"]

        if "full_name" in update_data:
            db_user.full_name = update_data["full_name"]

        if "default_veterinary_unit_id" in update_data:
            db_user.default_veterinary_unit_id = update_data["default_veterinary_unit_id"]

        if "is_active" in update_data:
            db_user.is_active = update_data["is_active"]

        if "password" in update_data and update_data["password"]:
            db_user.password_hash = get_password_hash(update_data["password"])

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return UserRead.model_validate(db_user)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Optional[User]:
        user = (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )
        if not user:
            return None
        if not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def create_role(self, role_in: RoleCreate) -> RoleRead:
        db_role = Role(
            name=role_in.name,
            description=role_in.description,
        )
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return RoleRead.model_validate(db_role)

    def list_roles(self) -> List[RoleRead]:
        roles = (
            self.db.query(Role)
            .order_by(Role.id.asc())
            .all()
        )
        return [RoleRead.model_validate(role) for role in roles]

    def get_role(self, role_id: int) -> Optional[RoleRead]:
        role = self.db.query(Role).get(role_id)
        if not role:
            return None
        return RoleRead.model_validate(role)

    def update_role(self, role_id: int, role_in: RoleUpdate) -> Optional[RoleRead]:
        db_role = self.db.query(Role).get(role_id)
        if not db_role:
            return None

        update_data = role_in.model_dump(exclude_unset=True)

        if "name" in update_data:
            db_role.name = update_data["name"]
        if "description" in update_data:
            db_role.description = update_data["description"]

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)

        return RoleRead.model_validate(db_role)

    def assign_role(self, obj_in: UserRoleCreate) -> UserRoleRead:
        db_user_role = UserRole(
            user_id=obj_in.user_id,
            role_id=obj_in.role_id,
            veterinary_unit_id=obj_in.veterinary_unit_id,
        )
        self.db.add(db_user_role)
        self.db.commit()
        self.db.refresh(db_user_role)
        return UserRoleRead.model_validate(db_user_role)

    def list_user_roles(self, user_id: int) -> List[UserRoleRead]:
        user_roles = (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id)
            .order_by(UserRole.id.asc())
            .all()
        )
        return [UserRoleRead.model_validate(ur) for ur in user_roles]
