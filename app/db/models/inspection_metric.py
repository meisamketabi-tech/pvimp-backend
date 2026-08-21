from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionMetric(Base):

    __tablename__ = "inspection_metrics"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    value = Column(
        String(200)
    )
