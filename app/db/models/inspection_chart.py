from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionChart(Base):

    __tablename__ = "inspection_charts"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    chart_type = Column(
        String(100)
    )
