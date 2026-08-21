from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISLaboratoryResult(Base):
    __tablename__ = "gis_laboratory_results"

    id = Column(Integer, primary_key=True, index=True)

    # SendSampleVCode
    send_sample_vcode = Column(
        String(100),
        unique=True,
        index=True,
    )

    # شماره جواب
    answer_no = Column(String(100))

    # تاریخ جواب
    answer_date = Column(Date)

    # تاریخ نمونه برداری
    sampling_date = Column(Date)

    # تاریخ ثبت
    register_date = Column(Date)

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

    # نوع واحد اپیدمیولوژیک
    epidemiology_unit_type = Column(String(100))

    # کد استان
    province_code = Column(String(20))

    # استان
    province_name = Column(String(100))

    # کد شهرستان
    county_code = Column(String(20))

    # شهرستان
    county_name = Column(String(100))

    # کد آزمایشگاه
    laboratory_code = Column(String(100))

    # نوع نمونه
    sample_type = Column(String(100))

    # تعداد نمونه
    sample_count = Column(Integer)

    # نام آزمایشگاه
    laboratory_name = Column(String(255))

    # نوع آزمایشگاه
    laboratory_type = Column(String(100))

    # مالک آزمایشگاه
    laboratory_owner = Column(String(100))

    # نوع دام
    animal_type = Column(String(100))

    # FK داخلی بیماری
    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        index=True,
    )

    # نام بیماری
    disease_name = Column(String(255))

    # وضعیت جواب
    result_status = Column(String(100))

    # X
    latitude = Column(Float)

    # Y
    longitude = Column(Float)

    # نام عامل جداشونده اول
    isolate_name_1 = Column(String(255))

    # نام عامل جداشونده دوم
    isolate_name_2 = Column(String(255))

    # A
    serotype_a = Column(String(50))

    # O
    serotype_o = Column(String(50))

    # Asia1
    serotype_asia1 = Column(String(50))

    # موارد غیر قابل قبول
    unacceptable_cases = Column(String(500))

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")
