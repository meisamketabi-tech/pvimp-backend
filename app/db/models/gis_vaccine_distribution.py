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


class GISVaccineDistribution(Base):

    __tablename__ = "gis_vaccine_distributions"

    id = Column(Integer, primary_key=True, index=True)

    distribution_vaccine_center_vcode = Column(String(100), unique=True, index=True)

    distribution_no = Column(String(100))

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    province_name = Column(String(100))
    county_name = Column(String(100))

    epidemiology_unit_code = Column(String(100))
    epidemiology_unit_name = Column(String(255))
    epidemiology_unit_type = Column(String(100))

    distribution_type = Column(String(100))
    distribution_status_id = Column(Integer)

    distribution_date = Column(Date)

    destination_province = Column(String(100))
    destination_county = Column(String(100))

    destination_unit_code = Column(String(100))
    destination_unit_name = Column(String(255))
    destination_unit_type = Column(String(100))

    vaccine_type = Column(String(100))
    vaccine_brand = Column(String(255))
    manufacturer = Column(String(255))
    batch_number = Column(String(100))

    vaccine_status = Column(String(100))
    vaccine_shape = Column(String(100))

    package_count = Column(Integer)
    dose_volume = Column(Float)
    unit_name = Column(String(100))

    user_code = Column(String(100))
    user_name = Column(String(255))

    registration_date = Column(Date)

    epidemiology_unit = relationship(
        "GISEpidemiologyUnit"
    )
