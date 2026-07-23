from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Approval(Base):

    __tablename__="approvals"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    requested_by=Column(Integer)

    approved_by=Column(Integer)

    status=Column(String(50))

    comment=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
