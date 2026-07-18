from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionArchive(Base):

    __tablename__ = "inspection_archives"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    archive_path = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
