from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationResponsibility(Base):

    __tablename__ = "organization_responsibilities"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False,
        index=True,
    )


    inspection_type_id = Column(
        Integer,
        ForeignKey("inspection_types.id"),
        nullable=False,
        index=True,
    )


    title = Column(
        String(300),
        nullable=False,
    )


    description = Column(
        String(1000),
        nullable=True,
    )


    priority = Column(
        Integer,
        default=1,
        nullable=False,
    )


    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )


    organization_unit = relationship(
        "OrganizationUnit",
    )


    inspection_type = relationship(
        "InspectionType",
    )
