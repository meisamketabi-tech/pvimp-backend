from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionPlan(Base):

    __tablename__ = "inspection_plans"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    description = Column(
        String(1000)
    )


    start_date = Column(
        DateTime
    )


    end_date = Column(
        DateTime
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
