from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISOutbreak(Base):
    __tablename__ = "gis_outbreaks"

    id = Column(Integer, primary_key=True, index=True)

    outbreak_no = Column(String(100), unique=True, index=True)

    disease_id = Column(
        Integer,
        ForeignKey("gis_diseases.id"),
        nullable=False,
    )

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=False,
    )

    start_date = Column(Date)

    end_date = Column(Date)

    status = Column(String(50))

    description = Column(Text)

    disease = relationship("GISDisease")

    epidemiology_unit = relationship("GISEpidemiologyUnit")