from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISSample(Base):
    __tablename__ = "gis_samples"

    id = Column(Integer, primary_key=True, index=True)

    sample_no = Column(String(100), unique=True, nullable=False, index=True)

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

    laboratory_id = Column(
        Integer,
        ForeignKey("gis_laboratories.id"),
    )

    sample_date = Column(Date)

    status = Column(String(50))

    epidemiology_unit = relationship("GISEpidemiologyUnit")

    disease = relationship("GISDisease")

    animal_type = relationship("GISAnimalType")

    laboratory = relationship("GISLaboratory")