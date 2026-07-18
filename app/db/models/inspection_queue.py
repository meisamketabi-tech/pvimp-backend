from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionQueue(Base):

    __tablename__ = "inspection_queues"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    priority = Column(
        Integer,
        default=1
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
