from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportRow(Base):
    __tablename__ = "gis_import_rows"

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

    raw_data = Column(
        JSON,
        nullable=False,
    )

    status = Column(
        String(30),
        default="PENDING",
    )

    job = relationship(
        "GISImportJob",
        backref="rows",
    )
