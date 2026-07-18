from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionFollowUp(Base):

    __tablename__ = "inspection_followups"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    followup_date = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )