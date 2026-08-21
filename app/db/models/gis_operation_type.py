from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class GISOperationType(Base):
    __tablename__ = "gis_operation_types"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(30), unique=True, nullable=False)

    title = Column(String(150), nullable=False)

    description = Column(String(255))