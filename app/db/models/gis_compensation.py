from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISCompensation(Base):
    __tablename__ = "gis_compensation"

    id = Column(Integer, primary_key=True, index=True)

    culling_id = Column(
        Integer,
        ForeignKey("gis_culling.id"),
        nullable=False,
    )

    payment_date = Column(Date)

    approved_animals = Column(Integer, default=0)

    amount = Column(Numeric(18, 2), default=0)

    culling = relationship("GISCulling")