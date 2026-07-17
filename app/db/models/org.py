from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Province(Base):
    __tablename__ = "province"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)

    counties = relationship("County", back_populates="province")


class County(Base):
    __tablename__ = "county"

    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)

    province = relationship("Province", back_populates="counties")
    veterinary_units = relationship("VeterinaryUnit", back_populates="county")


class VeterinaryUnit(Base):
    __tablename__ = "veterinary_unit"

    id = Column(Integer, primary_key=True, index=True)
    county_id = Column(Integer, ForeignKey("county.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    unit_type = Column(String(30), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    county = relationship("County", back_populates="veterinary_units")
    users = relationship("User", back_populates="default_veterinary_unit")
    user_roles = relationship("UserRole", back_populates="veterinary_unit")
