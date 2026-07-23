from sqlalchemy import Column,Integer,String

from app.core.database import Base


class RouteStop(Base):

    __tablename__="route_stops"


    id=Column(Integer,primary_key=True)

    route_id=Column(Integer)

    unit_id=Column(Integer)

    order_no=Column(Integer)

    status=Column(String(50))
