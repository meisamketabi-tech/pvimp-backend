from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Province(Base):
    __tablename__ = "province"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    code = Column(
        String(10),
        nullable=False,
        unique=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    counties = relationship(
        "County",
        back_populates="province",
    )


class County(Base):
    __tablename__ = "county"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    province_id = Column(
        Integer,
        ForeignKey("province.id"),
        nullable=False,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    code = Column(
        String(10),
        nullable=False,
        unique=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    province = relationship(
        "Province",
        back_populates="counties",
    )