from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class EventLog(Base):

    __tablename__="event_logs"


    id=Column(Integer,primary_key=True)

    event_type=Column(String(100))

    source=Column(String(100))

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    payload=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
