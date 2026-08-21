from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionDeadline(Base):

    __tablename__ = "inspection_deadlines"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id")
    )


    deadline = Column(
        DateTime,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
