from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class UserAssignment(Base):
    __tablename__ = "user_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    position_id = Column(
        Integer,
        ForeignKey("organization_positions.id"),
        nullable=False
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=True
    )

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    user = relationship(
        "UserAccount",
        back_populates="assignments"
    )

    organization_unit = relationship(
        "OrganizationUnit",
        backref="user_assignments"
    )

    position = relationship(
        "OrganizationPosition",
        back_populates="assignments"
    )
