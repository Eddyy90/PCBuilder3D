from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

# Criação do banco de dados (configuração diretamente aqui no api.py)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/dbname')

# Criação da engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Sessão local para as interações com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Criar as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# Criando o modelo para a tabela 'parts'
class PartInDB(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)
    description = Column(String)
    category = Column(String)

# Criando a instância da aplicação FastAPI
app = FastAPI()

# Montando o diretório estático
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Definir um modelo para a peça (Pydantic, usado para validar as requisições)
class Part(BaseModel):
    id: int
    name: str
    model: str
    description: str
    category: str

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criando uma API para retornar as peças do banco de dados
@app.get("/api/parts", response_model=list[Part])
async def get_parts(db: Session = Depends(get_db)):
    # Consulta todas as peças da tabela 'parts' no banco de dados
    parts = db.query(PartInDB).all()
    return parts

# Rota para servir o index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
