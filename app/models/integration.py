from sqlalchemy import Column,Integer,String,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Integration(Base):

    __tablename__="integrations"


    id=Column(Integer,primary_key=True)

    system_name=Column(String(200))

    endpoint=Column(String(500))

    api_key=Column(String(500))

    active=Column(Boolean,default=True)

    last_sync=Column(
        DateTime,
        server_default=func.now()
    )
