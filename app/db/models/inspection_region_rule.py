from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionRegionRule(Base):

    __tablename__ = "inspection_region_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    region = Column(
        String(200)
    )


    rule = Column(
        String(500)
    )
