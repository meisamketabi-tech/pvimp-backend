from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class InspectionChecklist(Base):

    __tablename__="inspection_checklists"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    category=Column(String(100))

    items=Column(Text)

    active=Column(Boolean,default=True)
