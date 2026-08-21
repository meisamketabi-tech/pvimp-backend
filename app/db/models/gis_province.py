from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISProvince(Base):
    __tablename__ = "gis_provinces"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    province_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    province_name = Column(
        String(100),
        nullable=False,
        index=True,
    )

    counties = relationship(
        "GISCounty",
        back_populates="province",
    )
