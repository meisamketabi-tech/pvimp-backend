
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from app.db.base_class import Base


class GISDiseaseOccurrence(Base):

    __tablename__ = "gis_disease_occurrences"

    id = Column(Integer, primary_key=True, index=True)

    occurrence_vcode = Column(
        String,
        index=True
    )

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True
    )

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        nullable=True,
        index=True
    )

    province_name = Column(String)
    county_name = Column(String)

    occurrence_date = Column(Date)

    animal_type = Column(String)

    affected_animals = Column(Integer)
    infected_animals = Column(Integer)
    dead_animals = Column(Integer)

    source_type = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    user_code = Column(String)
    user_name = Column(String)

    description = Column(Text)
