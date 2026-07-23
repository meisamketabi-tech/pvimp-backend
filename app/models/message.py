from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Message(Base):

    __tablename__="messages"


    id=Column(Integer,primary_key=True)

    sender_id=Column(Integer)

    receiver_id=Column(Integer)

    subject=Column(String(300))

    body=Column(Text)

    read=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
