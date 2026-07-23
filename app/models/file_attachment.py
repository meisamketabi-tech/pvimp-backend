from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class FileAttachment(Base):

    __tablename__="file_attachments"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    file_name=Column(String(300))

    file_path=Column(String(500))

    mime_type=Column(String(100))

    uploaded_by=Column(Integer)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
