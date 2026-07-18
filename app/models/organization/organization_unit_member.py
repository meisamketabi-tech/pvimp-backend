from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitMember(Base):
    __tablename__ = "organization_unit_members"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False
    )

    role_id = Column(
        Integer,
        ForeignKey("organization_roles.id"),
        nullable=False
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    organization_unit = relationship(
        "OrganizationUnit",
        backref="members"
    )
