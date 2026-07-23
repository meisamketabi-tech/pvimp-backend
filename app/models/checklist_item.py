from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class ChecklistItem(Base):

    __tablename__="checklist_items"


    id=Column(Integer,primary_key=True)

    checklist_id=Column(Integer)

    question=Column(String(500))

    item_type=Column(String(50))

    required=Column(Boolean,default=False)

    order_no=Column(Integer)
