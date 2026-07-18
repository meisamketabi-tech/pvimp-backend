from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationResponsibility(Base):
    __tablename__ = "organization_responsibilities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    category = Column(
        String(100),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    units = relationship(
        "OrganizationUnitResponsibility",
        back_populates="responsibility"
    )
