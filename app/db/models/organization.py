from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationUnit(Base):

    __tablename__ = "organization_units"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    name = Column(
        String(150),
        nullable=False,
    )


    code = Column(
        String(200),
        nullable=False,
        unique=True,
        index=True,
    )


    unit_type = Column(
        String(200),
        nullable=False,
    )


    type_id = Column(
        Integer,
        ForeignKey("organization_unit_types.id"),
        nullable=True,
        index=True,
    )


    level_id = Column(
        Integer,
        ForeignKey("organization_levels.id"),
        nullable=True,
        index=True,
    )


    parent_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=True,
    )


    province_id = Column(
        Integer,
        ForeignKey("province.id"),
        nullable=True,
    )


    county_id = Column(
        Integer,
        ForeignKey("county.id"),
        nullable=True,
    )


    description = Column(
        Text,
        nullable=True,
    )


    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    parent = relationship(
        "OrganizationUnit",
        remote_side=[id],
        back_populates="children",
    )


    children = relationship(
        "OrganizationUnit",
        back_populates="parent",
        cascade="all, delete-orphan",
    )


    organization_unit_type = relationship(
        "OrganizationUnitType",
    )


    organization_level = relationship(
        "OrganizationLevel",
    )


    province = relationship(
        "Province",
    )


    county = relationship(
        "County",
    )


    assignments = relationship(
        "UserAssignment",
        back_populates="organization_unit",
        cascade="all, delete-orphan",
    )
