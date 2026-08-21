from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionReminder(Base):

    __tablename__ = "inspection_reminders"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    message = Column(
        String(500)
    )


    remind_at = Column(
        DateTime
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
