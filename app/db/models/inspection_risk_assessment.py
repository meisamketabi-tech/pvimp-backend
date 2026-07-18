from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionRiskAssessment(Base):

    __tablename__ = "inspection_risk_assessments"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    risk_level = Column(
        String(50)
    )


    description = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
