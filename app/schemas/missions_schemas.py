from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from app.schemas.targets_schemas import TargetResponse


class MissionBase(BaseModel):
    is_complete: Optional[bool] = False
    targets: List[Dict[str, Union[str, bool]]] = Field(..., min_length=1, max_length=3)

class MissionCreate(MissionBase):
    cat_id: int

class MissionUpdate(BaseModel):
    is_complete: Optional[bool] = False

class MissionResponse(MissionBase):
    id: int
    cat_id: int
    targets: List[TargetResponse]

    class Config:
        orm_mode = True
