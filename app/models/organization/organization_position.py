from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationPosition(Base):
    __tablename__ = "organization_positions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    position_type = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
