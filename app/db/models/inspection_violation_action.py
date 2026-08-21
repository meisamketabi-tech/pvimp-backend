from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionViolationAction(Base):

    __tablename__ = "inspection_violation_actions"


    id = Column(
        Integer,
        primary_key=True
    )


    violation_id = Column(
        Integer
    )


    action = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
