from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionLock(Base):

    __tablename__ = "inspection_locks"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    locked_by = Column(
        Integer
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
