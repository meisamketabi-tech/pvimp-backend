from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class OrganizationUnitType(Base):

    __tablename__ = "organization_unit_types"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    code = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    level_order = Column(
        Integer,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
