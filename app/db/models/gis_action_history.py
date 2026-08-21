from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISActionHistory(Base):
    __tablename__ = "gis_action_history"

    id = Column(Integer, primary_key=True, index=True)

    operation_type_id = Column(
        Integer,
        ForeignKey("gis_operation_types.id"),
        nullable=False,
    )

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        nullable=False,
    )

    reference_table = Column(String(100))

    reference_id = Column(Integer)

    action = Column(String(100))

    description = Column(Text)

    created_at = Column(DateTime, server_default=func.now())

    operation_type = relationship("GISOperationType")

    epidemiology_unit = relationship("GISEpidemiologyUnit")