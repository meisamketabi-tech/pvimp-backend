from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    Index,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccinationPerformance(Base):
    """
    GIS Vaccination Performance

    هر رکورد یک عملیات/ثبت واکسیناسیون است.
    control_action_vaccine_vcode در داده واقعی الزاماً یکتا نیست؛
    بنابراین فقط برای جستجو/Join ایندکس می‌شود و UNIQUE نیست.
    """

    __tablename__ = "gis_vaccination_performances"

    id = Column(Integer, primary_key=True, index=True)

    control_action_vaccine_vcode = Column(
        String(100),
        unique=False,
        index=True,
        nullable=True,
    )
    vaccination_no = Column(String(100), index=True, nullable=True)

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    epidemiology_unit = relationship(
        "GISEpidemiologyUnit",
        foreign_keys=[epidemiology_unit_id],
        lazy="joined",
    )

    province_code = Column(String(20), index=True, nullable=True)
    province_name = Column(String(100), index=True, nullable=True)
    county_code = Column(String(20), index=True, nullable=True)
    county_name = Column(String(100), index=True, nullable=True)
    epidemiology_unit_name = Column(String(255), index=True, nullable=True)
    epidemiology_unit_code = Column(String(100), index=True, nullable=True)
    epidemiology_unit_type = Column(String(100), index=True, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    vaccination_center_name = Column(String(255), index=True, nullable=True)
    vaccination_center_code = Column(String(100), index=True, nullable=True)

    vaccine_type = Column(String(100), index=True, nullable=True)
    vaccine_brand = Column(String(255), index=True, nullable=True)
    manufacturer = Column(String(255), index=True, nullable=True)
    vaccine_category = Column(String(100), index=True, nullable=True)
    batch_number = Column(String(100), index=True, nullable=True)

    animal_type = Column(String(100), index=True, nullable=True)
    age_group = Column(String(100), index=True, nullable=True)

    vaccination_date = Column(Date, index=True, nullable=True)
    registration_date = Column(Date, index=True, nullable=True)

    rappel_vaccination = Column(String(100), index=True, nullable=True)
    operation_type = Column(String(100), index=True, nullable=True)

    total_animals = Column(Integer, nullable=True)
    animal_count = Column(Integer, nullable=True)
    eligible_animals = Column(Integer, nullable=True)
    vaccinated_animals = Column(Integer, nullable=True)

    dose_per_vial = Column(Float, nullable=True)
    package_count = Column(Integer, nullable=True)

    disease_name = Column(String(255), index=True, nullable=True)

    shock_after_injection = Column(Boolean, nullable=True)
    shock_count = Column(Integer, nullable=True)
    death_count = Column(Integer, nullable=True)
    abortion = Column(Boolean, nullable=True)
    abortion_count = Column(Integer, nullable=True)
    hypersensitivity = Column(Boolean, nullable=True)
    hypersensitivity_count = Column(Integer, nullable=True)
    local_complication = Column(Boolean, nullable=True)
    local_complication_count = Column(Integer, nullable=True)

    __table_args__ = (
        Index("ix_gis_vacc_perf_vaccine_province", "vaccine_type", "province_code"),
        Index("ix_gis_vacc_perf_vaccine_county", "vaccine_type", "county_code"),
        Index("ix_gis_vacc_perf_vaccine_unit", "vaccine_type", "epidemiology_unit_id"),
        Index("ix_gis_vacc_perf_unit_date", "epidemiology_unit_id", "vaccination_date"),
        Index(
            "ix_gis_vacc_perf_unit_vaccine_date",
            "epidemiology_unit_id",
            "vaccine_type",
            "vaccination_date",
        ),
        Index(
            "ix_gis_vacc_perf_province_county_date",
            "province_code",
            "county_code",
            "vaccination_date",
        ),
        Index("ix_gis_vacc_perf_vaccine_date", "vaccine_type", "vaccination_date"),
    )
