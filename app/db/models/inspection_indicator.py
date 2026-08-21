from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionIndicator(Base):

    __tablename__ = "inspection_indicators"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    target = Column(
        String(200)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
