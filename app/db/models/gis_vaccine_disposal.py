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


class GISVaccineDisposal(Base):

    __tablename__ = "gis_vaccine_disposals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Excel: DistributionVaccineCenterVCode
    distribution_vaccine_center_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    # Excel: شماره توزیع
    distribution_no = Column(String(100))

    # System FK
    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    # Excel: استان
    province_name = Column(String(100))

    # Excel: شهرستان
    county_name = Column(String(100))

    # Excel: تاریخ توزیع
    distribution_date = Column(Date)

    # Excel: DistributionStatusId
    distribution_status_id = Column(Integer)

    # Excel: استان واحد مقصد
    destination_province = Column(String(100))

    # Excel: شهر واحد مقصد
    destination_county = Column(String(100))

    # Excel: کد واحد مقصد
    destination_unit_code = Column(String(100))

    # Excel: نام واحد مقصد
    destination_unit_name = Column(String(255))

    # Excel: نوع واحد مقصد
    destination_unit_type = Column(String(100))

    # Excel: نوع واکسن
    vaccine_type = Column(String(100))

    # Excel: نام تجاری واکسن
    vaccine_brand = Column(String(255))

    # Excel: کارخانه سازنده
    manufacturer = Column(String(255))

    # Excel: سری ساخت
    batch_number = Column(String(100))

    # Excel: وضعیت
    vaccine_status = Column(String(100))

    # Excel: شکل واکسن
    vaccine_shape = Column(String(100))

    # Excel: تعداد بسته
    package_count = Column(Integer)

    # Excel: حجم/ دز هر بسته
    dose_volume = Column(Float)

    # Excel: واحد
    unit_name = Column(String(100))

    # Excel: کد کاربر
    user_code = Column(String(100))

    # Excel: نام کاربر
    user_name = Column(String(255))

    # Excel: تاریخ ثبت
    registration_date = Column(Date)

    # Excel: نوع واحد اپیدمیولوژیک
    epidemiology_unit_type = Column(String(100))

    # Excel: کد واحد اپیدمیولوژیک
    epidemiology_unit_code = Column(String(100))

    # Excel: نام واحد اپیدمیولوژیک
    epidemiology_unit_name = Column(String(255))

    # Excel: نوع توزیع
    distribution_type = Column(String(100))

    epidemiology_unit = relationship("GISEpidemiologyUnit")
