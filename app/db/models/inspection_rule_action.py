from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionRuleAction(Base):

    __tablename__ = "inspection_rule_actions"


    id = Column(
        Integer,
        primary_key=True
    )


    rule_id = Column(
        Integer
    )


    action = Column(
        String(500)
    )
