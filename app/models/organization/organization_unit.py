from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnit(Base):
    __tablename__ = "organization_units"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    parent_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=True
    )

    type_id = Column(
        Integer,
        ForeignKey("organization_unit_types.id"),
        nullable=False
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(200),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    parent = relationship(
        "OrganizationUnit",
        remote_side=[id],
        backref="children"
    )

    type = relationship(
        "OrganizationUnitType",
        back_populates="organization_units"
    )
