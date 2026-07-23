from sqlalchemy import Column,Integer,String,Date,String

from app.core.database import Base


class InspectionTask(Base):

    __tablename__="inspection_tasks"


    id=Column(Integer,primary_key=True)

    plan_id=Column(Integer)

    unit_id=Column(Integer)

    inspector_id=Column(Integer)

    status=Column(String(50))

    scheduled_date=Column(Date)
