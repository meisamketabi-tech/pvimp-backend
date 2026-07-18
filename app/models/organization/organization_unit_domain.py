from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class OrganizationUnitDomain(Base):
    __tablename__ = "organization_unit_domains"

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

    functional_domain_id = Column(
        Integer,
        ForeignKey("functional_domains.id"),
        nullable=False
    )
