from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class FunctionalDomain(Base):
    __tablename__ = "functional_domains"

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

    name = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
