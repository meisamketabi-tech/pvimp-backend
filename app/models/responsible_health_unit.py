
from sqlalchemy import Column,Integer,String,Boolean,Text

from app.core.database import Base



class ResponsibleHealthUnit(Base):

    __tablename__="responsible_health_units"


    id=Column(
        Integer,
        primary_key=True
    )


    name=Column(
        String(200)
    )


    unit_type=Column(
        String(100)
    )


    owner_name=Column(
        String(200)
    )


    address=Column(
        Text
    )


    phone=Column(
        String(50)
    )


    active=Column(
        Boolean,
        default=True
    )

