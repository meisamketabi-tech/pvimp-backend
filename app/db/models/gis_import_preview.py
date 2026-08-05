from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportPreview(Base):
    __tablename__ = "gis_import_preview"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_id = Column(
        Integer,
        ForeignKey("gis_import_jobs.id"),
        nullable=False,
        index=True,
    )

    row_number = Column(
        Integer,
        nullable=False,
    )

    preview_data = Column(
        JSON,
        nullable=False,
    )

    job = relationship(
        "GISImportJob",
        backref="previews",
    )
