from sqlalchemy import Column,Integer,Date,String

from app.core.database import Base


class InspectionCalendar(Base):

    __tablename__="inspection_calendar"


    id=Column(Integer,primary_key=True)

    inspector_id=Column(Integer)

    inspection_id=Column(Integer)

    planned_date=Column(Date)

    priority=Column(String(50))
