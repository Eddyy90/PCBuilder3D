from sqlalchemy import Column, Integer, String
from .database_connection import Base

class PartInDB(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    category = Column(String, nullable=False)
    model_url = Column(String, nullable=False)  # caminho do arquivo 3D
