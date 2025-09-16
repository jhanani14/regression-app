from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ Pydantic v2 replacement for orm_mode


class DatasetOut(BaseModel):
    id: int
    name: str
    columns: List[str]

    class Config:
        from_attributes = True   # ✅


class ExperimentOut(BaseModel):
    id: int
    metrics: Dict[str, float]

    class Config:
        from_attributes = True   # ✅
