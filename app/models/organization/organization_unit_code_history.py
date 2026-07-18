from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitCodeHistory(Base):
    __tablename__ = "organization_unit_code_histories"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    old_code = Column(
        String(50),
        nullable=False
    )

    new_code = Column(
        String(50),
        nullable=False
    )

    changed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
