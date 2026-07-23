
from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base



class HealthTraining(Base):

    __tablename__="health_trainings"


    id=Column(
        Integer,
        primary_key=True
    )


    title=Column(
        String(200)
    )


    target_group=Column(
        String(200)
    )


    instructor=Column(
        String(200)
    )


    training_date=Column(
        Date
    )


    location=Column(
        String(200)
    )


    description=Column(
        Text
    )


    active=Column(
        Boolean,
        default=True
    )

