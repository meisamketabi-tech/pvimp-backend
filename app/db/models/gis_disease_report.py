from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class GISDiseaseReport(Base):
    __tablename__ = "gis_disease_reports"

    id = Column(Integer, primary_key=True, index=True)

    # Source data can contain repeated observation-detail vcodes.
    # Keep this indexed for lookup, but do not enforce UNIQUE at DB level.
    observation_detail_vcode = Column(String(100), unique=False, index=True)
    observation_vcode = Column(String(100), index=True)

    province_code = Column(String(20), index=True)
    province_name = Column(String(100))
    county_code = Column(String(20), index=True)
    county_name = Column(String(100))

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=True,
        index=True,
    )
    epidemiology_unit_code = Column(String(50), index=True)
    epidemiology_unit_name = Column(String(255))
    epidemiology_unit_type = Column(String(100))

    disease_id = Column(Integer, ForeignKey("gis_diseases.id"), nullable=True, index=True)
    disease_name = Column(String(255), index=True)
    animal_type = Column(String(100))

    disease_start_date = Column(Date, nullable=True)
    total_animals = Column(Integer)
    infected_count = Column(Integer)
    death_count = Column(Integer)
    slaughtered_count = Column(Integer)
    sampling = Column(String(100))
    destroyed_count = Column(Integer)

    old_system_id = Column(String(100), index=True)
    age_group = Column(String(100))
    old_unit_code = Column(String(50), index=True)

    biting_animal = Column(String(100))
    operation_license_type = Column(String(255))
    creator_user_code = Column(String(50), index=True)
    creator_user_name = Column(String(255))
    source_unit_code = Column(String(50), index=True)
    source_unit_name = Column(String(255))
    source_unit_type = Column(String(100))

    epidemiology_unit = relationship("GISEpidemiologyUnit")
    disease = relationship("GISDisease")
