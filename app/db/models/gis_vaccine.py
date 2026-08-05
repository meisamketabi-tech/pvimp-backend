from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISVaccine(Base):
    __tablename__ = "gis_vaccines"

    id = Column(Integer, primary_key=True, index=True)

    vaccine_name = Column(String(200), nullable=False)

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        nullable=False,
    )

    manufacturer_id = Column(
        Integer,
        ForeignKey("gis_manufacturers.id"),
    )

    batch_no = Column(String(100))

    production_date = Column(Date)

    expire_date = Column(Date)

    dose_per_vial = Column(Integer)

    vaccine_type = Column(String(100))

    disease = relationship("GISDisease")

    manufacturer = relationship("GISManufacturer")