from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    mobile = Column(String(20), nullable=True, unique=True, index=True)
    default_veterinary_unit_id = Column(Integer, ForeignKey("veterinary_unit.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    password_hash = Column(String(255), nullable=False)

    default_veterinary_unit = relationship(
        "VeterinaryUnit",
        back_populates="users",
    )
    roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class UserRole(Base):
    __tablename__ = "user_role"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role_id",
            "veterinary_unit_id",
            name="uq_user_role_veterinary_unit",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    veterinary_unit_id = Column(Integer, ForeignKey("veterinary_unit.id"), nullable=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_roles")
    veterinary_unit = relationship("VeterinaryUnit", back_populates="user_roles")
