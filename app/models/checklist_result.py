from sqlalchemy import Column,Integer,String,Text

from app.core.database import Base


class ChecklistResult(Base):

    __tablename__="checklist_results"


    id=Column(Integer,primary_key=True)

    inspection_id=Column(Integer)

    item_id=Column(Integer)

    answer=Column(String(100))

    note=Column(Text)
