from pydantic import BaseModel

class PartBase(BaseModel):
    name: str
    description: str
    category: str
    model_url: str  # caminho do arquivo 3D

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int

    class Config:
        orm_mode = True
