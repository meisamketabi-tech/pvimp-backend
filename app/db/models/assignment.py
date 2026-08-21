from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class UserAssignment(Base):

    __tablename__ = "user_assignments"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_unit_id",
            "organization_unit_position_id",
            "is_active",
            name="uq_active_user_assignment_position",
        ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False,
    )


    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False,
    )


    organization_unit_position_id = Column(
        Integer,
        ForeignKey("organization_unit_positions.id"),
        nullable=True,
    )


    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
    )


    is_primary = Column(
        Boolean,
        nullable=False,
        default=False,
    )


    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    start_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


    end_date = Column(
        DateTime,
        nullable=True,
    )


    user = relationship(
        "User",
        back_populates="assignments",
    )


    organization_unit = relationship(
        "OrganizationUnit",
        back_populates="assignments",
    )


    organization_unit_position = relationship(
        "OrganizationUnitPosition",
        back_populates="assignments",
    )


    role = relationship(
        "Role",
        back_populates="assignments",
    )