from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Disease(Base):

    __tablename__="diseases"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    scientific_name=Column(String(300))

    category=Column(String(100))

    description=Column(Text)

    zoonotic=Column(Boolean,default=False)

    active=Column(Boolean,default=True)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
