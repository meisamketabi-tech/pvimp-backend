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

    distribution_vaccine_center_vcode = Column(String(100), index=True)

    epidemiology_unit_id = Column(
        Integer, ForeignKey("gis_epidemiology_units.id"), index=True
    )

    province_name = Column(String)

    county_name = Column(String)

    epidemiology_unit_type = Column(String)

    epidemiology_unit_code = Column(String)

    epidemiology_unit_name = Column(String)

    user_code = Column(String)

    user_name = Column(String)

    distribution_no = Column(String(100))

    distribution_date = Column(Date)

    vaccine_type = Column(String)

    vaccine_brand = Column(String)

    manufacturer = Column(String)

    batch_number = Column(String)

    vaccine_shape = Column(String)

    package_count = Column(Integer)

    dose_volume = Column(Float)

    unit_name = Column(String)

    registration_date = Column(Date)

    production_import_date = Column(Date)

    expiration_date = Column(Date)

    epidemiology_unit = relationship("GISEpidemiologyUnit")
