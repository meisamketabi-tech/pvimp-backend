
from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base



class CorrectiveActionPlan(Base):

    __tablename__="corrective_action_plans"


    id=Column(
        Integer,
        primary_key=True
    )


    violation_id=Column(
        Integer
    )


    responsible_person=Column(
        String(150)
    )


    action_description=Column(
        Text
    )


    due_date=Column(
        Date
    )


    status=Column(
        String(50),
        default="باز"
    )


    completed=Column(
        Boolean,
        default=False
    )

