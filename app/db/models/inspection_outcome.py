from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionOutcome(Base):

    __tablename__ = "inspection_outcomes"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    code = Column(
        String(50)
    )
