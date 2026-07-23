from sqlalchemy import Column,Integer,String,Boolean,Text

from app.core.database import Base


class Checklist(Base):

    __tablename__="checklists"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    category=Column(String(100))

    description=Column(Text)

    active=Column(Boolean,default=True)
