from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSendSampleDetail(Base):
    __tablename__ = "gis_send_sample_details"

    id = Column(Integer, primary_key=True, index=True)

    send_sample_detail_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    send_sample_vcode = Column(
        String(100),
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

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        index=True,
    )

    disease_name = Column(String(255))

    animal_type = Column(String(100))

    sample_type = Column(String(100))

    sample_count = Column(Integer)

    sampling_date = Column(Date)

    result_status = Column(String(100))

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")
