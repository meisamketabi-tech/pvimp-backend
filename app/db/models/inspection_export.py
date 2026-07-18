from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionExport(Base):

    __tablename__ = "inspection_exports"


    id = Column(
        Integer,
        primary_key=True
    )


    format = Column(
        String(50)
    )


    file_path = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
