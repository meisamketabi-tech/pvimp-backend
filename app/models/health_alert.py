
from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base



class HealthAlert(Base):

    __tablename__="health_alerts"


    id=Column(
        Integer,
        primary_key=True
    )


    alert_type=Column(
        String(100)
    )


    severity=Column(
        String(50)
    )


    title=Column(
        String(200)
    )


    message=Column(
        Text
    )


    source=Column(
        String(100)
    )


    status=Column(
        String(50),
        default="فعال"
    )


    created_at=Column(
        DateTime,
        server_default=func.now()
    )

