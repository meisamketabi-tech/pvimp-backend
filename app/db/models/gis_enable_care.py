from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISEnableCare(Base):

    __tablename__ = "gis_enable_cares"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # شناسه فرم
    enable_care_detail_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    enable_care_vcode = Column(
        String(100),
        index=True,
    )

    # موقعیت جغرافیایی
    province_code = Column(
        String(20),
    )

    province_name = Column(
        String(100),
    )

    county_code = Column(
        String(20),
    )

    county_name = Column(
        String(100),
    )

    # واحد اپیدمیولوژیک
    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    epidemiology_unit_code = Column(
        String(50),
    )

    epidemiology_unit_name = Column(
        String(255),
    )

    epidemiology_unit_type = Column(
        String(100),
    )

    # مراقبت
    care_type = Column(
        String(255),
    )

    animal_type = Column(
        String(100),
    )

    # تاریخ
    care_date = Column(
        Date,
    )

    # آمار
    total_animals = Column(
        Integer,
    )

    positive_count = Column(
        Integer,
    )

    negative_count = Column(
        Integer,
    )

    suspicious_count = Column(
        Integer,
    )

    # اطلاعات سیستم قدیم
    old_system_id = Column(
        String(100),
        index=True,
    )

    age_group = Column(
        String(100),
    )

    old_unit_code = Column(
        String(50),
    )

    window_code = Column(
        String(100),
    )

    operation_license_type = Column(
        String(255),
    )

    # Relationship
    epidemiology_unit = relationship(
        "GISEpidemiologyUnit",
    )
