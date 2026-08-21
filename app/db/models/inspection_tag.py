from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionTag(Base):

    __tablename__ = "inspection_tags"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(100)
    )


    color = Column(
        String(50)
    )
