from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionNotificationLog(Base):

    __tablename__ = "inspection_notification_logs"


    id = Column(
        Integer,
        primary_key=True
    )


    recipient = Column(
        String(200)
    )


    message = Column(
        String(1000)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
