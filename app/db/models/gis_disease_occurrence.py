from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISDiseaseOccurrence(Base):
    __tablename__ = "gis_disease_occurrences"

    id = Column(Integer, primary_key=True, index=True)

    # شناسه‌های فرم
    observation_detail_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    observation_vcode = Column(
        String(100),
        index=True,
    )

    # موقعیت جغرافیایی
    province_id = Column(
        Integer,
        ForeignKey("gis_provinces.id"),
        index=True,
    )

    county_id = Column(
        Integer,
        ForeignKey("gis_counties.id"),
        index=True,
    )

    province_code = Column(String(20))
    province_name = Column(String(100))

    county_code = Column(String(20))
    county_name = Column(String(100))

    # واحد اپیدمیولوژیک
    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    epidemiology_unit_code = Column(String(50))
    epidemiology_unit_name = Column(String(255))
    epidemiology_unit_type = Column(String(100))

    # بیماری
    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        index=True,
    )

    disease_name = Column(String(255))

    # دام
    animal_type = Column(String(100))

    # تاریخ‌ها

    start_date = Column(
        Date,
        nullable=True,
    )

    report_date = Column(
        Date,
        nullable=True,
    )

    registration_date = Column(
        Date,
        nullable=True,
    )

    # زمان ثبت سیستمی رکورد در دیتابیس

    registered_at = Column(
        DateTime,
        server_default=func.now(),
    )

    # آمار دام
    animal_count = Column(Integer)

    exposed_count = Column(Integer)

    infected_count = Column(Integer)

    dead_count = Column(Integer)

    slaughtered_count = Column(Integer)

    total_animals = Column(Integer)

    # نمونه‌برداری
    sample_taken = Column(
        Boolean,
        default=False,
    )

    # گزارش
    report_number = Column(
        String(100),
        index=True,
    )

    report_info = Column(Text)

    # مختصات
    latitude = Column(Float)

    longitude = Column(Float)

    # اطلاعات کاربر
    user_name = Column(String(100))

    user_code = Column(String(50))

    expert_names = Column(String(255))

    status = Column(String(50))

    # اطلاعات سیستم قدیم
    window_code = Column(String(100))

    operation_license_type = Column(String(255))

    old_system_id = Column(
        String(100),
        index=True,
    )

    description = Column(Text)

    # Relationships
    province = relationship("GISProvince")

    county = relationship("GISCounty")

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")
