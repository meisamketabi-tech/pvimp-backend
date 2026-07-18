from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionTypeRule(Base):

    __tablename__ = "inspection_type_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_type = Column(
        String(200)
    )


    rule_text = Column(
        String(500)
    )
