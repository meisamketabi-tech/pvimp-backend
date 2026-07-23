from sqlalchemy import Column,Integer,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class InspectionResponse(Base):

    __tablename__="inspection_responses"


    id=Column(Integer,primary_key=True)

    form_id=Column(Integer)

    unit_id=Column(Integer)

    inspector_id=Column(Integer)

    response_json=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
