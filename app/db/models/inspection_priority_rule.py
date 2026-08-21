from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionPriorityRule(Base):

    __tablename__ = "inspection_priority_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    weight = Column(
        Integer,
        default=1
    )
