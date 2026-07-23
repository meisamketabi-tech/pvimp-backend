from sqlalchemy import Column,Integer,String,Date,Float

from app.core.database import Base


class InspectionRoute(Base):

    __tablename__="inspection_routes"


    id=Column(Integer,primary_key=True)

    inspector_id=Column(Integer)

    title=Column(String(300))

    start_point=Column(String(300))

    end_point=Column(String(300))

    distance=Column(Float)

    planned_date=Column(Date)
