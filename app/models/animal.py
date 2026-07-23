from sqlalchemy import Column,Integer,String,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Animal(Base):

    __tablename__="animals"


    id=Column(Integer,primary_key=True)

    species=Column(String(100))

    breed=Column(String(100))

    owner_id=Column(Integer)

    identification_code=Column(String(100))

    health_status=Column(String(100))

    active=Column(Boolean,default=True)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
