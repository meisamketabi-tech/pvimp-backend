from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class VeterinaryUnit(Base):
    __tablename__ = "veterinary_units"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    code = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True
    )

    county_id = Column(
        Integer,
        ForeignKey("county.id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    county = relationship(
        "County"
    )

    inspections = relationship(
        "Inspection",
        back_populates="veterinary_unit"
    )