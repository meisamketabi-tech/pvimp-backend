from sqlalchemy import Column,Integer,String,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class ReportSchedule(Base):

    __tablename__="report_schedules"


    id=Column(Integer,primary_key=True)

    report_type=Column(String(200))

    frequency=Column(String(100))

    receiver=Column(String(300))

    active=Column(Boolean,default=True)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
