from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class Farm(Base):

    __tablename__="farms"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    owner_name=Column(String(200))

    farm_type=Column(String(100))

    address=Column(Text)

    registration_code=Column(String(100))

    active=Column(Boolean,default=True)
