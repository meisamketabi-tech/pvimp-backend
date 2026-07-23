from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base


class WorkOrder(Base):

    __tablename__="work_orders"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    order_type=Column(String(100))

    requester_id=Column(Integer)

    assigned_to=Column(Integer)

    description=Column(Text)

    priority=Column(String(50))

    due_date=Column(Date)

    completed=Column(Boolean,default=False)
