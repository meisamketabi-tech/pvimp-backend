from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionSourceType(Base):

    __tablename__ = "inspection_source_types"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    code = Column(
        String(50)
    )
