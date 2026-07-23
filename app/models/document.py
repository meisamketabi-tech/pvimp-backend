from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Document(Base):

    __tablename__="documents"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    document_type=Column(String(100))

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    file_path=Column(String(500))

    description=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
