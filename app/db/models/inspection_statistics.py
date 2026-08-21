from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionStatistics(Base):

    __tablename__ = "inspection_statistics"


    id = Column(
        Integer,
        primary_key=True
    )


    metric = Column(
        String(200)
    )


    value = Column(
        Integer,
        default=0
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
