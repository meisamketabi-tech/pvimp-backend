from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Permission(Base):

    __tablename__ = "permissions"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    code = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )


    title = Column(
        String(200),
        nullable=False,
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


    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )