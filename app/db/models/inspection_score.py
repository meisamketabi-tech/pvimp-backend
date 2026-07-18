from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionScore(Base):

    __tablename__ = "inspection_scores"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey(
            "inspections.id"
        ),
        nullable=False
    )


    total_score = Column(
        Integer,
        default=0
    )


    max_score = Column(
        Integer,
        default=0
    )