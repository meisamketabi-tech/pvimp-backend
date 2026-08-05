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
        index=True
    )

    distribution_vaccine_center_vcode = Column(
        String,
        index=True
    )

    distribution_no = Column(
        String(100)
    )

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey(
            "gis_epidemiology_units.id"
        ),
        index=True
    )

    province_name = Column(String)

    county_name = Column(String)


    distribution_date = Column(Date)


    distribution_status_id = Column(
        Integer
    )


    destination_province = Column(String)

    destination_county = Column(String)

    destination_unit_code = Column(String)

    destination_unit_name = Column(String)

    destination_unit_type = Column(String)


    vaccine_type = Column(String)

    vaccine_brand = Column(String)

    manufacturer = Column(String)

    batch_number = Column(String)


    vaccine_shape = Column(String)


    package_count = Column(Integer)

    dose_volume = Column(Float)


    unit_name = Column(String)


    user_code = Column(String)

    user_name = Column(String)


    registration_date = Column(Date)


    disposal_status = Column(
        String(100)
    )

    disposal_date = Column(
        Date
    )

    disposal_reason = Column(
        String(500)
    )


    epidemiology_unit = relationship(
        "GISEpidemiologyUnit"
    )