from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportColumn(Base):
    __tablename__ = "gis_import_columns"

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

    column_name = Column(
        String(255),
        nullable=False,
    )

    data_type = Column(
        String(50),
        default="STRING",
    )

    is_required = Column(
        Integer,
        default=0,
    )

    position = Column(
        Integer,
        nullable=False,
    )

    template = relationship(
        "GISImportTemplate",
        backref="columns",
    )
