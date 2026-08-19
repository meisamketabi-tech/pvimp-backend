from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccineInventory(Base):

    __tablename__ = "gis_vaccine_inventories"

    id = Column(Integer, primary_key=True, index=True)

    distribution_vaccine_center_vcode = Column(String(100), unique=True, index=True)

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    province_name = Column(String(100))
    county_name = Column(String(100))

    epidemiology_unit_type = Column(String(100))
    epidemiology_unit_code = Column(String(100))
    epidemiology_unit_name = Column(String(255))

    user_code = Column(String(100))
    user_name = Column(String(255))

    distribution_no = Column(String(100))
    distribution_date = Column(Date)

    vaccine_type = Column(String(1000))
    vaccine_brand = Column(String(255))
    manufacturer = Column(String(255))
    batch_number = Column(String(100))

    vaccine_shape = Column(String(100))

    package_count = Column(Integer)
    dose_volume = Column(Float)
    unit_name = Column(String(100))

    registration_date = Column(Date)

    production_import_date = Column(Date)
    expiration_date = Column(Date)

    epidemiology_unit = relationship("GISEpidemiologyUnit")
