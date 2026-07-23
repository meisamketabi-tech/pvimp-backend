from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class ServiceRequest(Base):

    __tablename__="service_requests"


    id=Column(Integer,primary_key=True)

    requester_id=Column(Integer)

    request_type=Column(String(100))

    subject=Column(String(300))

    description=Column(Text)

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
