from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSlaughterDisposal(Base):
    __tablename__ = "gis_slaughter_disposals"

    id = Column(Integer, primary_key=True, index=True)

    # ControlActionEmhaDetailVCode
    control_action_emha_detail_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    # ControlActionEmhaVCode
    control_action_emha_vcode = Column(
        String(100),
        index=True,
    )

    # کد استان
    province_code = Column(String(20))

    # استان
    province_name = Column(String(100))

    # کد شهرستان
    county_code = Column(String(20))

    # شهرستان
    county_name = Column(String(100))

    # FK داخلی
    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    # کد واحد اپیدمیولوژیک
    epidemiology_unit_code = Column(String(50))

    # نام واحد اپیدمیولوژیک
    epidemiology_unit_name = Column(String(255))

    # کد واحد قدیم
    old_unit_code = Column(String(50))

    # نوع واحد اپیدمیولوژیک
    epidemiology_unit_type = Column(String(100))

    # نوع دام
    animal_type = Column(String(100))

    # تاریخ کشتار/معدوم سازی
    action_date = Column(Date)

    # تعداد دام موجود
    total_animals = Column(Integer)

    # تعداد مثبت
    positive_count = Column(Integer)

    # تعداد دام کشتار شده
    slaughtered_count = Column(Integer)

    # تعداد دام معدوم شده
    destroyed_count = Column(Integer)

    # تعداد تلفات
    dead_count = Column(Integer)

    # مبلغ غرامت پیش بینی شده
    estimated_compensation = Column(Numeric(18, 2))

    # FK داخلی بیماری
    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        index=True,
    )

    # نوع بیماری / مراقبت
    disease_name = Column(String(255))

    # کد پنجره
    window_code = Column(String(100))

    # نوع پروانه بهره برداری
    operation_license_type = Column(String(255))

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")
