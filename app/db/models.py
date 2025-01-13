from sqlalchemy import Column, Integer, String
from .database_connection import Base

class PartInDB(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)
    description = Column(String)
    category = Column(String)
    model_url = Column(String)

