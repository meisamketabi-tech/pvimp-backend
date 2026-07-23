from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Attachment(Base):

    __tablename__="attachments"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    file_name=Column(String(300))

    file_path=Column(String(500))

    uploaded_at=Column(
        DateTime,
        server_default=func.now()
    )
