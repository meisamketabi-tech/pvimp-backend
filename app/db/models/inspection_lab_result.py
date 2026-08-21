from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionLabResult(Base):

    __tablename__ = "inspection_lab_results"

    id = Column(
        Integer,
        primary_key=True
    )

    lab_request_id = Column(
        Integer,
        ForeignKey("inspection_lab_requests.id")
    )

    result = Column(
        String(500)
    )

    status = Column(
        String(50),
        default="completed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
