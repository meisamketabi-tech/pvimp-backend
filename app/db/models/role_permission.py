from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base



class RolePermission(Base):

    __tablename__ = "role_permissions"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
    )


    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=False,
    )


    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    role = relationship(
        "Role",
        back_populates="role_permissions",
    )


    permission = relationship(
        "Permission",
        back_populates="role_permissions",
    )