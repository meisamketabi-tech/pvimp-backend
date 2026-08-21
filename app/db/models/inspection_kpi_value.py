from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionKPIValue(Base):

    __tablename__ = "inspection_kpi_values"


    id = Column(
        Integer,
        primary_key=True
    )


    kpi_id = Column(
        Integer
    )


    value = Column(
        Integer
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
