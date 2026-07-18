from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionComment(Base):

    __tablename__ = "inspection_comments"


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


    comment = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )