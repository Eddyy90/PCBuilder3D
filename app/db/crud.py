from sqlalchemy.orm import Session
from . import models
from .schemas import PartCreate

def create_part(db: Session, part: PartCreate):
    db_part = models.PartInDB(
        name=part.name,
        model=part.model,
        description=part.description,
        category=part.category,
        model_url=part.model_url
    )
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

def get_parts(db: Session):
    return db.query(models.PartInDB).all()

def get_part_by_id(db: Session, part_id: int):
    return db.query(models.PartInDB).filter(models.PartInDB.id == part_id).first()

def update_part(db: Session, part_id: int, part: PartCreate):
    db_part = db.query(models.PartInDB).filter(models.PartInDB.id == part_id).first()
    if db_part:
        db_part.name = part.name
        db_part.model = part.model
        db_part.description = part.description
        db_part.category = part.category
        db_part.model_url = part.model_url
        db.commit()
        db.refresh(db_part)
    return db_part

def delete_part(db: Session, part_id: int):
    db_part = db.query(models.PartInDB).filter(models.PartInDB.id == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
    return db_part
