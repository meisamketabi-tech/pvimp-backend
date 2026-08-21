from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionSchedule(Base):

    __tablename__ = "inspection_schedules"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_type_id = Column(
        Integer,
        ForeignKey(
            "inspection_types.id"
        ),
        nullable=False
    )


    organization_unit_id = Column(
        Integer,
        ForeignKey(
            "organization_units.id"
        ),
        nullable=False
    )


    scheduled_date = Column(
        DateTime,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )