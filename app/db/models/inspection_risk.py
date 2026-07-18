from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.db.base_class import Base


class InspectionRisk(Base):

    __tablename__ = "inspection_risks"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200),
        nullable=False
    )


    level = Column(
        Integer,
        default=1
    )
