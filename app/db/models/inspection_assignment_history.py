from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAssignmentHistory(Base):

    __tablename__ = "inspection_assignment_histories"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    assigned_from = Column(
        Integer
    )


    assigned_to = Column(
        Integer
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
