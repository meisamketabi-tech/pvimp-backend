from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password

from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition

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
            if query.filter(User.username == username).first():
                raise ValueError("Username already exists")

        if email:
            if query.filter(User.email == email).first():
                raise ValueError("Email already exists")

        if mobile:
            if query.filter(User.mobile == mobile).first():
                raise ValueError("Mobile already exists")


    def create_user(self, user_in: UserCreate) -> UserRead:

        self._ensure_unique_user_fields(
            user_in.username,
            user_in.email,
            user_in.mobile,
        )

        db_user = User(
            username=user_in.username,
            full_name=user_in.full_name,
            email=user_in.email,
            mobile=user_in.mobile,
            default_veterinary_unit_id=user_in.default_veterinary_unit_id,
            is_active=user_in.is_active,
            password_hash=get_password_hash(user_in.password),
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

        return [
            UserRead.model_validate(x)
            for x in users
        ]



    def get_user(self, user_id:int):

        user = self.db.query(User).get(user_id)

        if not user:
            return None

        return UserRead.model_validate(user)



    def authenticate_user(
        self,
        username:str,
        password:str,
    ):

        user = (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            return None

        if not user.is_active:
            return None

        if not verify_password(password,user.password_hash):
            return None

        return user



    def create_role(self, role_in:RoleCreate):

        role = Role(
            name=role_in.name,
            description=role_in.description,
        )

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return RoleRead.model_validate(role)



    def list_roles(self):

        roles = (
            self.db.query(Role)
            .order_by(Role.id.asc())
            .all()
        )

        return [
            RoleRead.model_validate(x)
            for x in roles
        ]



    def get_role(self, role_id:int):

        role=self.db.query(Role).get(role_id)

        if not role:
            return None

        return RoleRead.model_validate(role)



    def update_role(self, role_id:int, role_in:RoleUpdate):

        role=self.db.query(Role).get(role_id)

        if not role:
            return None

        data=role_in.model_dump(exclude_unset=True)

        for key,value in data.items():
            setattr(role,key,value)

        self.db.commit()
        self.db.refresh(role)

        return RoleRead.model_validate(role)



    def assign_role(
        self,
        obj_in: AssignmentCreate,
    ) -> AssignmentRead:


        if obj_in.organization_unit_position_id:

            occupied = (
                self.db.query(UserAssignment)
                .filter(
                    UserAssignment.organization_unit_position_id
                    == obj_in.organization_unit_position_id,
                    UserAssignment.is_active == True,
                )
                .first()
            )


            if occupied:

                raise ValueError(
                    "Organization position is already assigned"
                )



        assignment = UserAssignment(
            user_id=obj_in.user_id,
            role_id=obj_in.role_id,
            organization_unit_id=obj_in.organization_unit_id,
            organization_unit_position_id=obj_in.organization_unit_position_id,
            is_primary=obj_in.is_primary,
        )


        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)


        return AssignmentRead.model_validate(
            assignment
        )



    def list_user_roles(
        self,
        user_id:int,
    ):

        assignments = (
            self.db.query(UserAssignment)
            .filter(
                UserAssignment.user_id == user_id
            )
            .order_by(
                UserAssignment.id.asc()
            )
            .all()
        )

        return [
            AssignmentRead.model_validate(x)
            for x in assignments
        ]
