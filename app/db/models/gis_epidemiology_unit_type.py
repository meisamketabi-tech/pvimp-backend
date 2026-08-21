from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISEpidemiologyUnitType(Base):
    __tablename__ = "gis_epidemiology_unit_types"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    code = Column(
        String(50),
        unique=True,
        index=True,
    )

    description = Column(
        String(500),
    )

    units = relationship(
        "GISEpidemiologyUnit",
        back_populates="unit_type",
    )
