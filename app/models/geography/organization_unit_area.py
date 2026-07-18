from sqlalchemy import Column, Integer, ForeignKey

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
