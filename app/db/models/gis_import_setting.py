from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.db.base_class import Base


class GISImportSetting(Base):
    __tablename__ = "gis_import_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    key = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    value = Column(
        String(500),
    )

    description = Column(
        String(500),
    )

    is_active = Column(
        Boolean,
        default=True,
    )
