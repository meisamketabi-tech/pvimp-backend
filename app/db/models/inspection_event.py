from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionEvent(Base):

    __tablename__ = "inspection_events"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    event_type = Column(
        String(100)
    )


    description = Column(
        String(1000)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
