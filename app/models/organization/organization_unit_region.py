from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitRegion(Base):
    __tablename__ = "organization_unit_regions"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    region_id = Column(
        Integer,
        ForeignKey("organization_regions.id"),
        nullable=False
    )

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
