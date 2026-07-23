from sqlalchemy import Column,Integer,String,Text,Date

from app.core.database import Base


class EnforcementAction(Base):

    __tablename__="enforcement_actions"


    id=Column(Integer,primary_key=True)

    violation_id=Column(Integer)

    action_type=Column(String(100))

    legal_reference=Column(String(200))

    description=Column(Text)

    action_date=Column(Date)
