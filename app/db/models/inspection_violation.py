from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class InspectionViolation(Base):

    __tablename__ = "inspection_violations"

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

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    inspection = relationship(
        "Inspection"
    )