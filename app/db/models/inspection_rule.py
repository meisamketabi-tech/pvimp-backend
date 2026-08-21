from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionRule(Base):

    __tablename__ = "inspection_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    expression = Column(
        String(1000)
    )
