from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionTagRelation(Base):

    __tablename__ = "inspection_tag_relations"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    tag_id = Column(
        Integer
    )
