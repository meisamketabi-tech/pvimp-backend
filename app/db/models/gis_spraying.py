from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSpraying(Base):
    __tablename__ = "gis_spraying"

    id = Column(Integer, primary_key=True, index=True)

    spraying_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    province_code = Column(String(20))
    province_name = Column(String(100))

    county_code = Column(String(20))
    county_name = Column(String(100))

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    epidemiology_unit_code = Column(String(50))
    epidemiology_unit_name = Column(String(255))
    epidemiology_unit_type = Column(String(100))

    spraying_date = Column(Date)

    plan_type = Column(String(100))

    operation_type = Column(String(100))

    poison_type = Column(String(200))

    sprayed_area = Column(Numeric(12, 2))

    sprayed_animal_count = Column(Integer)

    animal_type = Column(String(100))

    total_animals = Column(Integer)

    epidemiology_unit = relationship("GISEpidemiologyUnit")
