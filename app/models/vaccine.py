from sqlalchemy import Column,Integer,String,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Vaccine(Base):

    __tablename__="vaccines"


    id=Column(Integer,primary_key=True)

    name=Column(String(200))

    manufacturer=Column(String(200))

    batch_number=Column(String(100))

    quantity=Column(Integer)

    expiration_date=Column(DateTime)

    active=Column(Boolean,default=True)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
