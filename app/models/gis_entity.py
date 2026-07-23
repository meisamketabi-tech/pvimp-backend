from sqlalchemy import Column,Integer,String,Float,Boolean

from app.core.database import Base


class GISEntity(Base):

    __tablename__="gis_entities"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    latitude=Column(Float)

    longitude=Column(Float)

    zone=Column(String(200))

    active=Column(Boolean,default=True)
