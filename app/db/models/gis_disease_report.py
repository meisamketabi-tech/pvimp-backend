from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISDiseaseReport(Base):
    __tablename__ = "gis_disease_reports"

    # Internal ID
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================
    # Excel Identification
    # =========================

    observation_detail_vcode = Column(
        String(100),
        index=True
    )

    observation_vcode = Column(
        String(100),
        index=True
    )


    # =========================
    # Geography
    # =========================

    province_code = Column(
        String(20),
        index=True
    )

    province_name = Column(
        String(100)
    )


    county_code = Column(
        String(20),
        index=True
    )

    county_name = Column(
        String(100)
    )


    # =========================
    # Epidemiology Unit
    # =========================

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey(
            "gis_epidemiology_units.id"
        ),
        nullable=True,
        index=True
    )

    epidemiology_unit_code = Column(
        String(50),
        index=True
    )

    epidemiology_unit_name = Column(
        String(255)
    )

    epidemiology_unit_type = Column(
        String(100)
    )


    # =========================
    # Disease
    # =========================

    disease_id = Column(
        Integer,
        ForeignKey(
            "gis_diseases.id"
        ),
        nullable=True,
        index=True
    )

    disease_name = Column(
        String(255),
        index=True
    )


    # =========================
    # Animal
    # =========================

    animal_type = Column(
        String(100)
    )


    # =========================
    # Disease Report Data
    # =========================

    disease_start_date = Column(
        Date
    )


    total_animals = Column(
        Integer
    )

    infected_count = Column(
        Integer
    )

    death_count = Column(
        Integer
    )

    slaughtered_count = Column(
        Integer
    )

    destroyed_count = Column(
        Integer
    )


    sampling = Column(
        String(100)
    )


    # =========================
    # Old System Information
    # =========================

    old_system_id = Column(
        String(100),
        index=True
    )

    old_unit_code = Column(
        String(50),
        index=True
    )

    age_group = Column(
        String(100)
    )


    # =========================
    # Other Information
    # =========================

    biting_animal = Column(
        String(100)
    )


    operation_license_type = Column(
        String(255)
    )


    # =========================
    # Creator User
    # =========================

    creator_user_code = Column(
        String(50),
        index=True
    )

    creator_user_name = Column(
        String(255)
    )


    # =========================
    # Source Unit
    # =========================

    source_unit_code = Column(
        String(50),
        index=True
    )

    source_unit_name = Column(
        String(255)
    )

    source_unit_type = Column(
        String(100)
    )


    # =========================
    # Relationships
    # =========================

    epidemiology_unit = relationship(
        "GISEpidemiologyUnit"
    )


    disease = relationship(
        "GISDisease"
    )