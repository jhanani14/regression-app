# app/schemas/dataset.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

# -------------------------
# Response schema for Dataset
# -------------------------
class DatasetOut(BaseModel):
    id: int
    name: str
    columns: List[str]            # list of column names in the dataset
    uploaded_at: datetime | None = None   # optional, include timestamp if needed

    class Config:
        from_attributes = True   # Pydantic v2 replacement for orm_mode
