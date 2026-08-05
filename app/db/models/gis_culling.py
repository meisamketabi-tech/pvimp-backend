from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISCulling(Base):
    __tablename__ = "gis_culling"

    id = Column(Integer, primary_key=True, index=True)

    outbreak_id = Column(
        Integer,
        ForeignKey("gis_outbreaks.id"),
        nullable=False,
    )

    animal_type_id = Column(
        Integer,
        ForeignKey("gis_animal_types.id"),
        nullable=False,
    )

    culling_date = Column(Date)

    positive_animals = Column(Integer, default=0)

    culled_animals = Column(Integer, default=0)

    dead_animals = Column(Integer, default=0)

    outbreak = relationship("GISOutbreak")

    animal_type = relationship("GISAnimalType")