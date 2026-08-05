from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccinationPerformance(Base):

    __tablename__ = "gis_vaccination_performances"

    id = Column(Integer, primary_key=True, index=True)

    control_action_vaccine_vcode = Column(String, index=True)

    epidemiology_unit_id = Column(
        Integer, ForeignKey("gis_epidemiology_units.id"), index=True
    )

    province_name = Column(String)
    county_name = Column(String)

    vaccination_date = Column(Date)
    registration_date = Column(Date)

    animal_type = Column(String)
    vaccine_type = Column(String)

    vaccine_brand = Column(String)
    manufacturer = Column(String)
    batch_number = Column(String)

    total_animals = Column(Integer)
    vaccinated_animals = Column(Integer)
    eligible_animals = Column(Integer)

    age_group = Column(String)

    disease_name = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    user_code = Column(String)
    user_name = Column(String)

    epidemiology_unit = relationship("GISEpidemiologyUnit")
