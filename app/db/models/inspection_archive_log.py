from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionArchiveLog(Base):

    __tablename__ = "inspection_archive_logs"


    id = Column(
        Integer,
        primary_key=True
    )


    archive_id = Column(
        Integer
    )


    action = Column(
        String(200)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
