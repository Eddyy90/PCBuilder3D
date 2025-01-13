from pydantic import BaseModel

class PartBase(BaseModel):
    name: str
    model: str
    description: str
    category: str
    model_url: str


class PartCreate(PartBase):
    pass


class Part(PartBase):
    id: int

    class Config:
        orm_mode = True
