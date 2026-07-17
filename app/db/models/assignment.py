from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserAssignment(Base):
    __tablename__ = "user_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False,
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False,
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=True,
    )

    end_date = Column(
        Date,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    user = relationship(
        "User",
        back_populates="assignments",
    )

    organization_unit = relationship(
        "OrganizationUnit",
        back_populates="assignments",
    )

    role = relationship(
        "Role",
        back_populates="assignments",
    )