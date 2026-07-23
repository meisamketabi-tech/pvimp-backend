from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class GISLayer(Base):

    __tablename__="gis_layers"


    id=Column(Integer,primary_key=True)

    name=Column(String(200))

    layer_type=Column(String(100))

    geojson=Column(Text)

    active=Column(Boolean,default=True)
