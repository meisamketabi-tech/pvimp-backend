from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionStatusLog(Base):

    __tablename__ = "inspection_status_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer
    )

    status = Column(
        String(100)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
