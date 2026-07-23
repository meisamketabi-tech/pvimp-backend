
from sqlalchemy import Column,Integer,String,Date,Boolean

from app.core.database import Base



class HealthReminder(Base):

    __tablename__="health_reminders"


    id=Column(
        Integer,
        primary_key=True
    )


    entity_type=Column(
        String(100)
    )


    entity_id=Column(
        Integer
    )


    title=Column(
        String(200)
    )


    due_date=Column(
        Date
    )


    completed=Column(
        Boolean,
        default=False
    )

