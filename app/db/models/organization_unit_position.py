from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationUnitPosition(Base):

    __tablename__ = "organization_unit_positions"

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

    organization_position_id = Column(
        Integer,
        ForeignKey("organization_positions.id"),
        nullable=False,
        index=True,
    )

    parent_assignment_id = Column(
        Integer,
        ForeignKey("organization_unit_positions.id"),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime,
        nullable=True,
    )


    organization_unit = relationship(
        "OrganizationUnit",
    )


    organization_position = relationship(
        "OrganizationPosition",
    )


    parent_assignment = relationship(
        "OrganizationUnitPosition",
        remote_side=[id],
    )


    assignments = relationship(
        "UserAssignment",
        back_populates="organization_unit_position",
    )
