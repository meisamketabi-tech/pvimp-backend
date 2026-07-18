from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from datetime import datetime

from app.db.base_class import Base


class InspectionLabRequest(Base):

    __tablename__ = "inspection_lab_requests"


    id = Column(
        Integer,
        primary_key=True
    )


    sample_id = Column(
        Integer,
        ForeignKey("inspection_samples.id")
    )


    status = Column(
        String(50),
        default="pending"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
