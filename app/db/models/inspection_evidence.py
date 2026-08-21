from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionEvidence(Base):

    __tablename__ = "inspection_evidences"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id")
    )


    evidence_type = Column(
        String(100)
    )


    file_path = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )