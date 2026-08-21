from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAlert(Base):

    __tablename__ = "inspection_alerts"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(300)
    )


    severity = Column(
        String(50)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
