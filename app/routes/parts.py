from fastapi import Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db import crud, database_connection
from db.schemas import PartCreate, Part
import os
from .api import app, templates, UPLOAD_DIR



# Criar nova peça com arquivo
@app.post("/api/parts/", response_model=Part, tags=["Parts"])
async def create_part(
    name: str = Form(...),
    description: str = Form(""),
    category: str = Form(...),
    model_file: UploadFile = File(...),
    db: Session = Depends(database_connection.get_db)
):
    file_path = os.path.join(UPLOAD_DIR, model_file.filename)
    with open(file_path, "wb") as f:
        f.write(await model_file.read())

    part_data = PartCreate(
        name=name,
        description=description,
        category=category,
        model_url=file_path
    )
    return crud.create_part(db=db, part=part_data)


# Listar todas as peças
@app.get("/api/parts", response_model=list[Part], tags=["Parts"])
async def get_parts(db: Session = Depends(database_connection.get_db)):
    """Lista todas as peças cadastradas"""
    return crud.get_parts(db)

# Buscar peça por ID
@app.get("/api/parts/{part_id}", response_model=Part, tags=["Parts"])
async def get_part(part_id: int, db: Session = Depends(database_connection.get_db)):
    db_part = crud.get_part_by_id(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part

# Atualizar peça por ID
@app.put("/api/parts/{part_id}", response_model=Part, tags=["Parts"])
async def update_part(part_id: int, part: PartCreate, db: Session = Depends(database_connection.get_db)):
    db_part = crud.update_part(db, part_id, part)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part

# Deletar peça por ID
@app.delete("/api/parts/{part_id}", response_model=Part, tags=["Parts"])
async def delete_part(part_id: int, db: Session = Depends(database_connection.get_db)):
    db_part = crud.delete_part(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part

# ---------------------
# Rotas de Frontend
# ---------------------

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def read_root(request: Request):
    """Página inicial com template Jinja2"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/parts/create", response_class=HTMLResponse, tags=["Frontend"])
async def create_part_form(request: Request):
    """Renderiza o formulário HTML para criar peça"""
    return templates.TemplateResponse("create_part.html", {"request": request})
