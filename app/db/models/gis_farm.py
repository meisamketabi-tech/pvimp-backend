from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISFarm(Base):
    __tablename__ = "gis_farms"

    id = Column(Integer, primary_key=True, index=True)

    farm_code = Column(String(50), unique=True, nullable=False, index=True)

    farm_name = Column(String(255), nullable=False)

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=False,
    )

    owner_name = Column(String(255))

    national_code = Column(String(20))

    phone = Column(String(30))

    address = Column(String(500))

    latitude = Column(Numeric(10, 7))

    longitude = Column(Numeric(10, 7))

    epidemiology_unit = relationship("GISEpidemiologyUnit")