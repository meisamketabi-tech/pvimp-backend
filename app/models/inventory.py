from sqlalchemy import Column,Integer,String,Float,Boolean

from app.core.database import Base


class Inventory(Base):

    __tablename__="inventories"


    id=Column(Integer,primary_key=True)

    item_code=Column(String(100))

    item_name=Column(String(300))

    category=Column(String(100))

    quantity=Column(Float)

    unit=Column(String(50))

    active=Column(Boolean,default=True)
