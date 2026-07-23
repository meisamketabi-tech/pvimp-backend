from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class KnowledgeBase(Base):

    __tablename__="knowledge_base"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    category=Column(String(100))

    content=Column(Text)

    source=Column(String(300))

    active=Column(Boolean,default=True)
