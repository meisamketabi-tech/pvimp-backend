from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccination(Base):
    __tablename__ = "gis_vaccinations"

    id = Column(Integer, primary_key=True, index=True)

    vaccination_no = Column(String(100), unique=True, index=True)

    vaccination_date = Column(Date, nullable=False)

    register_date = Column(Date)

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=False,
        index=True,
    )

    animal_type_id = Column(
        Integer,
        ForeignKey("gis_animal_types.id"),
        nullable=False,
    )

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        nullable=False,
    )

    vaccine_id = Column(
        Integer,
        ForeignKey("gis_vaccines.id"),
        nullable=False,
    )

    operation_type = Column(String(100))

    booster = Column(Integer, default=0)

    total_animals = Column(Integer, default=0)

    eligible_animals = Column(Integer, default=0)

    vaccinated_animals = Column(Integer, default=0)

    shock_count = Column(Integer, default=0)

    abortion_count = Column(Integer, default=0)

    reaction_count = Column(Integer, default=0)

    local_reaction_count = Column(Integer, default=0)

    death_count = Column(Integer, default=0)

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    animal_type = relationship("GISAnimalType")

    disease = relationship("GISDisease")

    vaccine = relationship("GISVaccine")