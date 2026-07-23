from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class Configuration(Base):

    __tablename__="configurations"


    id=Column(Integer,primary_key=True)

    key=Column(String(200))

    value=Column(Text)

    group_name=Column(String(100))

    description=Column(Text)

    active=Column(Boolean,default=True)
