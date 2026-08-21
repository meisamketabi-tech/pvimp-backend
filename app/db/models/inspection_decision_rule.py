from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionDecisionRule(Base):

    __tablename__ = "inspection_decision_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    condition = Column(
        String(1000)
    )


    decision = Column(
        String(500)
    )
