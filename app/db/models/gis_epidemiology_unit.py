from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.db.models.gis_province import GISProvince
from app.db.models.gis_county import GISCounty


class GISEpidemiologyUnit(Base):
    __tablename__ = "gis_epidemiology_units"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    unit_name = Column(
        String(255),
        nullable=False,
    )

    unit_code = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    old_code = Column(
        String(50),
    )

    window_code = Column(
        String(100),
    )

    unit_type_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_unit_types.id"),
        nullable=False,
        index=True,
    )

    province_id = Column(
        Integer,
        ForeignKey("gis_provinces.id"),
        index=True,
    )

    county_id = Column(
        Integer,
        ForeignKey("gis_counties.id"),
        index=True,
    )

    parent_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
    )

    latitude = Column(
        Float,
    )

    longitude = Column(
        Float,
    )

    user_name = Column(
        String(100),
    )

    user_code = Column(
        String(50),
    )

    sheep_count = Column(
        Integer,
        default=0,
    )

    cattle_count = Column(
        Integer,
        default=0,
    )

    goat_count = Column(
        Integer,
        default=0,
    )

    horse_count = Column(
        Integer,
        default=0,
    )

    dog_count = Column(
        Integer,
        default=0,
    )

    camel_count = Column(
        Integer,
        default=0,
    )

    buffalo_count = Column(
        Integer,
        default=0,
    )

    postal_code = Column(
        String(20),
    )

    sanitary_license_number = Column(
        String(100),
    )

    sanitary_license_date = Column(
        Date,
    )

    operation_license_number = Column(
        String(100),
    )

    operation_license_date = Column(
        Date,
    )

    address = Column(
        String(500),
    )

    license_type = Column(
        String(255),
    )

    has_sub_unit = Column(
        Boolean,
        default=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    unit_type = relationship(
        "GISEpidemiologyUnitType",
        back_populates="units",
    )

    province = relationship(
        "GISProvince",
        foreign_keys=[province_id],
    )

    county = relationship(
        "GISCounty",
        foreign_keys=[county_id],
    )

    parent = relationship(
        "GISEpidemiologyUnit",
        remote_side=[id],
    )
