from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionScheduleRule(Base):

    __tablename__ = "inspection_schedule_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    interval_days = Column(
        Integer
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
