from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitType(Base):
    __tablename__ = "organization_unit_types"

    id = Column(Integer, primary_key=True, index=True)

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

    description = Column(
        String(500),
        nullable=True
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

    organization_units = relationship(
        "OrganizationUnit",
        backref="type"
    )
