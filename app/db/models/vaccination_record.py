from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"

    id = Column(Integer, primary_key=True, index=True)

    action_no = Column(String(50), index=True)

    province = Column(String(100))

    county = Column(String(100))

    epi_code = Column(
        String(100),
        ForeignKey("gis_epidemiology_units.unit_code"),
        nullable=False,
        index=True,
    )

    vaccine_type = Column(String(100))

    animal_type = Column(String(100))

    vaccine_date = Column(String(10))

    vaccine_name = Column(String(255))

    manufacturer = Column(String(255))

    batch_no = Column(String(100))

    total_animals = Column(Integer)

    vaccinated_animals = Column(Integer)

    age_group = Column(String(100))

    operation_type = Column(String(100))

    description = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    epidemiology_unit = relationship(
        "GISEpidemiologyUnit"
    )