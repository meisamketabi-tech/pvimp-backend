from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationHierarchy(Base):
    __tablename__ = "organization_hierarchies"

    id = Column(Integer, primary_key=True, index=True)

    parent_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    child_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    level = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
