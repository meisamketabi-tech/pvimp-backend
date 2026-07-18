from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionExecution(Base):

    __tablename__ = "inspection_executions"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    executor_id = Column(
        Integer
    )


    started_at = Column(
        DateTime
    )


    finished_at = Column(
        DateTime
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
