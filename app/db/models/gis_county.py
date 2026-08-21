from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISCounty(Base):
    __tablename__ = "gis_counties"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    county_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    county_name = Column(
        String(100),
        nullable=False,
        index=True,
    )

    province_id = Column(
        Integer,
        ForeignKey("gis_provinces.id"),
        nullable=False,
        index=True,
    )

    province = relationship(
        "GISProvince",
        back_populates="counties",
    )
