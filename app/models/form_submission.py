from sqlalchemy import Column,Integer,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class FormSubmission(Base):

    __tablename__="form_submissions"


    id=Column(Integer,primary_key=True)

    form_id=Column(Integer)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    data=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
