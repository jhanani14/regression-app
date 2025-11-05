# app/schemas/algorithm.py
from pydantic import BaseModel
from typing import Dict, Literal

# -------------------------
# Individual algorithm details
# -------------------------
class AlgorithmDetail(BaseModel):
    type: Literal["classification", "regression"]  # type of algorithm
    description: str                                # brief description
    best_for: str                                   # recommended use case

# -------------------------
# API response containing all algorithms
# -------------------------
class AlgorithmInfoResponse(BaseModel):
    classification_algorithms: Dict[str, AlgorithmDetail]  # name -> details
    regression_algorithms: Dict[str, AlgorithmDetail]      # name -> details
