from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class InspectionAssignment(Base):

    __tablename__ = "inspection_assignments"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False,
    )


    inspector_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False,
    )


    assigned_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    inspection = relationship(
        "Inspection",
        back_populates="assignments",
    )


    inspector = relationship(
        "User",
    )