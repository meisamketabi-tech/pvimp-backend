from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class GISManufacturer(Base):
    __tablename__ = "gis_manufacturers"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    country = Column(String(100))