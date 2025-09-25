from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Literal, Optional


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


# ✅ NEW SCHEMA: AlgorithmInfo for API response
class AlgorithmDetail(BaseModel):
    type: Literal["classification", "regression"]
    description: str
    best_for: str


class AlgorithmInfoResponse(BaseModel):
    classification_algorithms: Dict[str, AlgorithmDetail]
    regression_algorithms: Dict[str, AlgorithmDetail]
