from pydantic import BaseModel
from typing import Optional


class TargetBase(BaseModel):
    name: str
    country: str
    notes: str
    is_complete: Optional[bool] = False

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = False

class TargetResponse(TargetBase):
    id: int
    mission_id: int

    class Config:
        orm_mode = True
