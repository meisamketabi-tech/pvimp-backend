from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAudit(Base):

    __tablename__ = "inspection_audits"


    id = Column(
        Integer,
        primary_key=True
    )


    user_id = Column(
        Integer
    )


    action = Column(
        String(200)
    )


    details = Column(
        String(1000)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
