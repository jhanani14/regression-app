# app/schemas/experiment.py
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

# -------------------------
# Response schema for Experiment
# -------------------------
class ExperimentOut(BaseModel):
    id: int
    created_at: datetime | None = None   # optional if you want to include timestamp
    metrics: Dict[str, float] = {}      # metric_name -> metric_value mapping

    class Config:
        from_attributes = True           # Pydantic v2 replacement for orm_mode
