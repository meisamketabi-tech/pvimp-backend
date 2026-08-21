from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISOperationHistory(Base):
    __tablename__ = "gis_operation_history"

    id = Column(Integer, primary_key=True, index=True)

    action_type_title = Column(String, index=True)

    action_no = Column(String, index=True)

    certificate_no = Column(String)

    action_date = Column(Date)

    registered_at = Column(DateTime, server_default=func.now())

    epidemiology_unit_id = Column(
        Integer,
        ForeignKey("gis_epidemiology_units.id"),
        index=True,
    )

    epidemiology_unit_code = Column(String)

    epidemiology_unit_name = Column(String)

    epidemiology_unit_type = Column(String)

    province_name = Column(String)

    county_name = Column(String)

    action_name = Column(String)

    report_date = Column(Date)

    report_info = Column(Text)
