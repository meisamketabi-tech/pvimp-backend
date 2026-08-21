from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionSyncLog(Base):

    __tablename__ = "inspection_sync_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    source = Column(
        String(100)
    )

    status = Column(
        String(50)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
