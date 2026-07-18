from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):

    __tablename__ = "user_account"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String(200),
        nullable=False,
        unique=True,
        index=True,
    )

    full_name = Column(
        String(255),
        nullable=True,
    )

    email = Column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    mobile = Column(
        String(20),
        nullable=True,
        unique=True,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    assignments = relationship(
        "UserAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
