from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionCorrection(Base):

    __tablename__ = "inspection_corrections"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    description = Column(
        String(1000)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
