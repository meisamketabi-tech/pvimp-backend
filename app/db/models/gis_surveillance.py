from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSurveillance(Base):
    __tablename__ = "gis_surveillance"

    id = Column(Integer, primary_key=True, index=True)

    surveillance_no = Column(String(100), unique=True, index=True)

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=False,
    )

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        nullable=False,
    )

    animal_type_id = Column(
        Integer,
        ForeignKey("gis_animal_types.id"),
        nullable=False,
    )

    surveillance_type = Column(String(100))

    surveillance_date = Column(Date)

    total_animals = Column(Integer, default=0)

    positive = Column(Integer, default=0)

    negative = Column(Integer, default=0)

    suspected = Column(Integer, default=0)

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")

    animal_type = relationship("GISAnimalType")