from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class AIAssistantLog(Base):

    __tablename__="ai_assistant_logs"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    question=Column(Text)

    answer=Column(Text)

    model=Column(String(100))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
