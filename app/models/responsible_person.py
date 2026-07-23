from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class ResponsiblePerson(Base):

    __tablename__="responsible_persons"


    id=Column(Integer,primary_key=True)

    unit_id=Column(Integer)

    name=Column(String(200))

    national_code=Column(String(50))

    phone=Column(String(50))

    active=Column(Boolean,default=True)
