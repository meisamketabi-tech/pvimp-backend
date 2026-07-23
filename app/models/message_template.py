from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class MessageTemplate(Base):

    __tablename__="message_templates"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    channel=Column(String(50))

    subject=Column(String(300))

    content=Column(Text)

    active=Column(Boolean,default=True)
