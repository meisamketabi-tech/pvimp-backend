from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class OrganizationRole(Base):

    __tablename__ = "organization_roles"

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

    description = Column(
        String(500),
        nullable=True,
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
