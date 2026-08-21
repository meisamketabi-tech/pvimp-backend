from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionDecision(Base):

    __tablename__ = "inspection_decisions"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id")
    )

    decision = Column(
        String(100)
    )

    reason = Column(
        String(500)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
