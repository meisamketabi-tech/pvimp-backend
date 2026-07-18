from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionHistory(Base):

    __tablename__ = "inspection_histories"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey(
            "inspections.id"
        )
    )


    action = Column(
        String(100),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )