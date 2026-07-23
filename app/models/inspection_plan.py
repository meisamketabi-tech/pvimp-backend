from sqlalchemy import Column,Integer,String,Date,Text,Boolean

from app.core.database import Base


class InspectionPlan(Base):

    __tablename__="inspection_plans"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    plan_type=Column(String(100))

    inspector_id=Column(Integer)

    start_date=Column(Date)

    end_date=Column(Date)

    description=Column(Text)

    active=Column(Boolean,default=True)
