from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportMapping(Base):
    __tablename__ = "gis_import_mapping"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    template_id = Column(
        Integer,
        ForeignKey("gis_import_templates.id"),
        nullable=False,
        index=True,
    )

    excel_column = Column(
        String(255),
        nullable=False,
    )

    database_field = Column(
        String(255),
        nullable=False,
    )

    transform_rule = Column(
        String(500),
    )

    template = relationship(
        "GISImportTemplate",
        backref="mappings",
    )
