from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationAssignment(Base):
    __tablename__ = "organization_assignments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
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

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    user = relationship(
        "UserAccount",
        backref="organization_assignments"
    )

    position = relationship(
        "OrganizationPosition",
        backref="assignments"
    )
