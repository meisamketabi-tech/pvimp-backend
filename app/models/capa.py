from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base


class CAPA(Base):

    __tablename__="capa_actions"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    action_type=Column(String(50))

    description=Column(Text)

    responsible_id=Column(Integer)

    due_date=Column(Date)

    completed=Column(Boolean,default=False)
