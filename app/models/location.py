from sqlalchemy import Column,Integer,String,Float,Boolean

from app.core.database import Base


class Location(Base):

    __tablename__="locations"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    location_type=Column(String(100))

    province=Column(String(100))

    city=Column(String(100))

    latitude=Column(Float)

    longitude=Column(Float)

    active=Column(Boolean,default=True)
