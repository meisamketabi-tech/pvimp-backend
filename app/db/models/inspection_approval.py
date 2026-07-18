from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionApproval(Base):

    __tablename__ = "inspection_approvals"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    approved_by = Column(
        Integer
    )


    status = Column(
        String(50)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
