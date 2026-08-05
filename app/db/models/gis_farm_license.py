from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISFarmLicense(Base):
    __tablename__ = "gis_farm_licenses"

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(
        Integer,
        ForeignKey("gis_farms.id"),
        nullable=False,
    )

    license_no = Column(String(100), nullable=False)

    license_type = Column(String(100))

    issue_date = Column(Date)

    expire_date = Column(Date)

    status = Column(String(50))

    farm = relationship("GISFarm")