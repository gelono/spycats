from pydantic import BaseModel


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int

class SpyCatCreate(SpyCatBase):
    pass

class SpyCatResponse(SpyCatBase):
    id: int

    class Config:
        orm_mode = True

class SpyCatUpdate(BaseModel):
    salary: float
