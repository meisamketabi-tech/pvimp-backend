from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class OrganizationPosition(Base):

    __tablename__ = "organization_positions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    level_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    is_managerial = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )
