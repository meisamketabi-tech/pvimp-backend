from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionSource(Base):

    __tablename__ = "inspection_sources"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    type = Column(
        String(100)
    )
