from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionNotification(Base):

    __tablename__ = "inspection_notifications"


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


    message = Column(
        String(500),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )