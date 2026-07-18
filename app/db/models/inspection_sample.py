from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from datetime import datetime

from app.db.base_class import Base


class InspectionSample(Base):

    __tablename__ = "inspection_samples"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )


    sample_code = Column(
        String(100),
        nullable=False
    )


    sample_type = Column(
        String(100)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
