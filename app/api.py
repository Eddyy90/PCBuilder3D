from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import crud, models, database_connection
from db.schemas import PartCreate, Part

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/api/parts", response_model=list[Part])
async def get_parts(db: Session = Depends(database_connection.get_db)):
    parts = crud.get_parts(db)
    return parts


@app.get("/api/parts/{part_id}", response_model=Part)
async def get_part(part_id: int, db: Session = Depends(database_connection.get_db)):
    db_part = crud.get_part_by_id(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part


@app.post("/api/parts/create", response_model=Part)
async def create_part(part: PartCreate, db: Session = Depends(database_connection.get_db)):
    created_part = crud.create_part(db=db, part=part)
    return created_part


@app.put("/api/parts/update/{part_id}", response_model=Part)
async def update_part(part_id: int, part: PartCreate, db: Session = Depends(database_connection.get_db)):
    db_part = crud.update_part(db, part_id, part)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part


@app.delete("/api/parts/delete/{part_id}", response_model=Part)
async def delete_part(part_id: int, db: Session = Depends(database_connection.get_db)):
    db_part = crud.delete_part(db, part_id)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_part


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
