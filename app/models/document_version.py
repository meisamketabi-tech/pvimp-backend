from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class DocumentVersion(Base):

    __tablename__="document_versions"


    id=Column(Integer,primary_key=True)

    document_id=Column(Integer)

    version_number=Column(Integer)

    file_path=Column(String(500))

    change_note=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
