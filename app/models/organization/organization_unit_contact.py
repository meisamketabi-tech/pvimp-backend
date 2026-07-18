from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitContact(Base):
    __tablename__ = "organization_unit_contacts"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    contact_name = Column(
        String(200),
        nullable=False
    )

    mobile = Column(
        String(50),
        nullable=True
    )

    email = Column(
        String(200),
        nullable=True
    )

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    organization_unit = relationship(
        "OrganizationUnit",
        backref="contacts"
    )
