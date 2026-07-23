from sqlalchemy import Column,Integer,String,Date,Boolean

from app.core.database import Base


class Schedule(Base):

    __tablename__="schedules"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    schedule_type=Column(String(100))

    assigned_to=Column(Integer)

    start_date=Column(Date)

    end_date=Column(Date)

    status=Column(String(50))

    active=Column(Boolean,default=True)
