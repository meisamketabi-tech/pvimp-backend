from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    Enum as SQLEnum,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.models.inspection import InspectionStatusEnum


class InspectionStatusHistory(Base):

    __tablename__ = "inspection_status_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )

    old_status = Column(
        SQLEnum(InspectionStatusEnum),
        nullable=True
    )

    new_status = Column(
        SQLEnum(InspectionStatusEnum),
        nullable=False
    )

    changed_by = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False
    )

    changed_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    note = Column(
        Text,
        nullable=True
    )

    inspection = relationship(
        "Inspection"
    )

    user = relationship(
        "User"
    )
