from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionKPI(Base):

    __tablename__ = "inspection_kpis"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    formula = Column(
        String(1000)
    )
