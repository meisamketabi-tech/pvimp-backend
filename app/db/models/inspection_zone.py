from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionZone(Base):

    __tablename__ = "inspection_zones"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    description = Column(
        String(500)
    )
