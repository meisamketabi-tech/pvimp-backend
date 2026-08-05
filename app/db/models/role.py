from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Role(Base):

    __tablename__ = "roles"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    name = Column(
        String(200),
        nullable=False,
        unique=True,
        index=True,
    )


    description = Column(
        Text,
        nullable=True,
    )


    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    assignments = relationship(
        "UserAssignment",
        back_populates="role",
        cascade="all, delete-orphan",
    )


    role_permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )