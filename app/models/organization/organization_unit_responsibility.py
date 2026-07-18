from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class OrganizationUnitResponsibility(Base):
    __tablename__ = "organization_unit_responsibilities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    responsibility_id = Column(
        Integer,
        ForeignKey("organization_responsibilities.id"),
        nullable=False
    )
