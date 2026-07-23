
from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base



class HealthPersonnel(Base):

    __tablename__="health_personnel"


    id=Column(
        Integer,
        primary_key=True
    )


    national_id=Column(
        String(20)
    )


    full_name=Column(
        String(200)
    )


    position=Column(
        String(100)
    )


    license_number=Column(
        String(100)
    )


    phone=Column(
        String(30)
    )


    active=Column(
        Boolean,
        default=True
    )

