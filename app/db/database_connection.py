import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/dbname"
)

# Engine e sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para criar tabelas
def init_db():
    from . import models  # importa todos os models para criar as tabelas
    Base.metadata.create_all(bind=engine)

# Dependency do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
