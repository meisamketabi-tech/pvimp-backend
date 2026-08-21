from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class GISAnimalType(Base):
    __tablename__ = "gis_animal_types"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False, unique=True)
    scientific_name = Column(String(150))
    is_active = Column(Integer, default=1)