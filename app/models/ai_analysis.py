from sqlalchemy import Column,Integer,String,Text,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class AIAnalysis(Base):

    __tablename__="ai_analyses"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    model_name=Column(String(200))

    input_data=Column(Text)

    result=Column(Text)

    confidence=Column(Float)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
