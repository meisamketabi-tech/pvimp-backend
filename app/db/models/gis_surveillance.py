from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSurveillance(Base):
    __tablename__ = "gis_surveillance"

    id = Column(Integer, primary_key=True, index=True)

    # EnableCareDetailVCode
    enable_care_detail_vcode = Column(String(100), unique=True, index=True)

    # EnableCareVCode
    enable_care_vcode = Column(String(100), index=True)

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

    surveillance_type = Column(String(100))

    animal_type = Column(String(100))

    surveillance_date = Column(Date)

    total_animals = Column(Integer)

    positive = Column(Integer)

    negative = Column(Integer)

    suspected = Column(Integer)

    old_system_id = Column(String(100))

    age_group = Column(String(100))

    old_unit_code = Column(String(50))

    window_code = Column(String(100))

    operation_license_type = Column(String(255))

    epidemiology_unit = relationship("GISEpidemiologyUnit")
