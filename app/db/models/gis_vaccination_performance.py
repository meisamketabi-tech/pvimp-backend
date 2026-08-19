from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    Boolean,
    ForeignKey,
    Index,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccinationPerformance(Base):
    """
    GIS Vaccination Performance

    هر رکورد نشان‌دهنده یک عملیات/ثبت واکسیناسیون است.

    ساختار مورد استفاده برای داشبورد:

        Vaccine
            └── Province
                └── County
                    └── Epidemiology Unit
                        └── Vaccination Operations / History

    بنابراین از همین جدول می‌توان وضعیت پوشش واکسیناسیون
    و همچنین تاریخچه عملیات هر واحد را استخراج کرد.
    """

    __tablename__ = "gis_vaccination_performances"

    # ============================================================
    # Primary Key
    # ============================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ============================================================
    # Operation / External Keys
    # ============================================================

    control_action_vaccine_vcode = Column(
        String(100),
        unique=True,
        index=True,
        nullable=True,
    )

    vaccination_no = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Epidemiology Unit Relation
    # ============================================================

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey(
            "gis_epidemiology_units.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    epidemiology_unit = relationship(
        "GISEpidemiologyUnit",
        foreign_keys=[epidemiology_unit_id],
        lazy="joined",
    )

    # ============================================================
    # Province
    # ============================================================

    province_code = Column(
        String(20),
        index=True,
        nullable=True,
    )

    province_name = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # County
    # ============================================================

    county_code = Column(
        String(20),
        index=True,
        nullable=True,
    )

    county_name = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Epidemiology Unit
    # ============================================================

    epidemiology_unit_name = Column(
        String(255),
        index=True,
        nullable=True,
    )

    epidemiology_unit_code = Column(
        String(100),
        index=True,
        nullable=True,
    )

    epidemiology_unit_type = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # GIS Coordinates
    # ============================================================

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )

    # ============================================================
    # Vaccination Center
    # ============================================================

    vaccination_center_name = Column(
        String(255),
        index=True,
        nullable=True,
    )

    vaccination_center_code = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Vaccine
    # ============================================================

    vaccine_type = Column(
        String(100),
        index=True,
        nullable=True,
    )

    vaccine_brand = Column(
        String(255),
        index=True,
        nullable=True,
    )

    manufacturer = Column(
        String(255),
        index=True,
        nullable=True,
    )

    vaccine_category = Column(
        String(100),
        index=True,
        nullable=True,
    )

    batch_number = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Animal
    # ============================================================

    animal_type = Column(
        String(100),
        index=True,
        nullable=True,
    )

    age_group = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Dates
    # ============================================================

    vaccination_date = Column(
        Date,
        index=True,
        nullable=True,
    )

    registration_date = Column(
        Date,
        index=True,
        nullable=True,
    )

    # ============================================================
    # Vaccination Operation
    # ============================================================

    rappel_vaccination = Column(
        String(100),
        index=True,
        nullable=True,
    )

    operation_type = Column(
        String(100),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Animal / Coverage Counts
    # ============================================================

    total_animals = Column(
        Integer,
        nullable=True,
    )

    animal_count = Column(
        Integer,
        nullable=True,
    )

    eligible_animals = Column(
        Integer,
        nullable=True,
    )

    vaccinated_animals = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Vaccine Consumption
    # ============================================================

    dose_per_vial = Column(
        Float,
        nullable=True,
    )

    package_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Disease
    # ============================================================

    disease_name = Column(
        String(255),
        index=True,
        nullable=True,
    )

    # ============================================================
    # Post Vaccination Shock
    # ============================================================

    shock_after_injection = Column(
        Boolean,
        nullable=True,
    )

    shock_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Death
    # ============================================================

    death_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Abortion
    # ============================================================

    abortion = Column(
        Boolean,
        nullable=True,
    )

    abortion_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Hypersensitivity
    # ============================================================

    hypersensitivity = Column(
        Boolean,
        nullable=True,
    )

    hypersensitivity_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Local Complication
    # ============================================================

    local_complication = Column(
        Boolean,
        nullable=True,
    )

    local_complication_count = Column(
        Integer,
        nullable=True,
    )

    # ============================================================
    # Composite Indexes
    # ============================================================
    #
    # این Indexها برای داشبورد سلسله‌مراتبی مهم هستند:
    #
    # Vaccine
    #   -> Province
    #       -> County
    #           -> Unit
    #               -> Date
    #
    # و همچنین برای نمایش تاریخچه عملیات یک واحد.
    # ============================================================

    __table_args__ = (
        # --------------------------------------------------------
        # Vaccine + Province
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_vaccine_province",
            "vaccine_type",
            "province_code",
        ),
        # --------------------------------------------------------
        # Vaccine + County
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_vaccine_county",
            "vaccine_type",
            "county_code",
        ),
        # --------------------------------------------------------
        # Vaccine + Unit
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_vaccine_unit",
            "vaccine_type",
            "epidemiology_unit_id",
        ),
        # --------------------------------------------------------
        # Unit + Vaccination Date
        #
        # برای نمایش تاریخچه عملیات واحد
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_unit_date",
            "epidemiology_unit_id",
            "vaccination_date",
        ),
        # --------------------------------------------------------
        # Unit + Vaccine + Date
        #
        # برای:
        # «تاریخچه این واحد برای این واکسن»
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_unit_vaccine_date",
            "epidemiology_unit_id",
            "vaccine_type",
            "vaccination_date",
        ),
        # --------------------------------------------------------
        # Province + County + Date
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_province_county_date",
            "province_code",
            "county_code",
            "vaccination_date",
        ),
        # --------------------------------------------------------
        # Vaccine + Date
        #
        # برای گزارش روند واکسیناسیون در طول زمان
        # --------------------------------------------------------
        Index(
            "ix_gis_vacc_perf_vaccine_date",
            "vaccine_type",
            "vaccination_date",
        ),
    )
