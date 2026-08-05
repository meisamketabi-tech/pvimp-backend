from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISLabResult(Base):
    __tablename__ = "gis_lab_results"

    id = Column(Integer, primary_key=True, index=True)

    sample_id = Column(
        Integer,
        ForeignKey("gis_samples.id"),
        nullable=False,
    )

    test_type = Column(String(100))

    result = Column(String(50))

    positive_count = Column(Integer, default=0)

    negative_count = Column(Integer, default=0)

    report_date = Column(Date)

    sample = relationship("GISSample")