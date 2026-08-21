from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitArea(Base):

    __tablename__ = "organization_unit_areas"


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


    geographic_area_id = Column(
        Integer,
        ForeignKey("geographic_areas.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    organization_unit = relationship(
        "OrganizationUnit",
        back_populates="geographic_areas"
    )


    geographic_area = relationship(
        "GeographicArea",
        back_populates="organization_units"
    )