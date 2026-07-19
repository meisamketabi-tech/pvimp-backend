from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db.base_class import Base


class InspectionAssignmentHistory(Base):

    __tablename__ = "inspection_assignment_histories"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )


    assigned_from = Column(
        Integer,
        nullable=True
    )


    assigned_to = Column(
        Integer,
        nullable=True
    )


    changed_by = Column(
        Integer,
        nullable=True
    )


    action = Column(
        String(50),
        nullable=False,
        default="ASSIGNED"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
