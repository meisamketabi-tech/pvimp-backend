from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitAddress(Base):
    __tablename__ = "organization_unit_addresses"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    address = Column(
        String(500),
        nullable=False
    )

    phone = Column(
        String(50),
        nullable=True
    )

    postal_code = Column(
        String(20),
        nullable=True
    )

    is_primary = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    organization_unit = relationship(
        "OrganizationUnit",
        backref="addresses"
    )
