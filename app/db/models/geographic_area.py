from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GeographicArea(Base):

    __tablename__ = "geographic_areas"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    parent_id = Column(
        Integer,
        ForeignKey("geographic_areas.id"),
        nullable=True
    )


    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )


    name = Column(
        String(200),
        nullable=False
    )


    area_type = Column(
        String(50),
        nullable=False
    )


    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    parent = relationship(
        "GeographicArea",
        remote_side=[id],
        back_populates="children"
    )


    children = relationship(
        "GeographicArea",
        back_populates="parent"
    )


    organization_units = relationship(
        "OrganizationUnitArea",
        back_populates="geographic_area",
        cascade="all, delete-orphan"
    )