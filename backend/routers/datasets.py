# backend/routers/datasets.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException
import pandas as pd
import io
from sqlalchemy.orm import Session
from datetime import datetime

from backend.deps import get_db, get_current_user
from backend.models import Dataset, DatasetFile

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload")
async def upload_dataset(file: UploadFile, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Upload CSV/XLSX file, store it in database, return dataset_id + columns for frontend.
    """
    try:
        if file.filename.endswith(".csv"):
            file_bytes = await file.read()
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file.filename.endswith(".xlsx"):
            file_bytes = await file.read()
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            raise HTTPException(status_code=400, detail="Only CSV/XLSX supported")

        dataset = Dataset(name=file.filename, user_id=user.id, uploaded_at=datetime.utcnow())
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        dataset_file = DatasetFile(dataset_id=dataset.id, filename=file.filename, data=file_bytes)
        db.add(dataset_file)
        db.commit()

        return {"dataset_id": dataset.id, "name": dataset.name, "columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}/columns")
def get_columns(dataset_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Return only the list of columns (legacy endpoint, still works).
    """
    dataset_file = db.query(DatasetFile).filter(DatasetFile.dataset_id == dataset_id).first()
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")
    try:
        df = pd.read_csv(io.BytesIO(dataset_file.data))
        return {"columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")


@router.get("/{dataset_id}/info")
def get_dataset_info(dataset_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Return both columns and their data types for auto-suggesting algorithms.
    """
    dataset_file = db.query(DatasetFile).filter(DatasetFile.dataset_id == dataset_id).first()
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")
    try:
        df = pd.read_csv(io.BytesIO(dataset_file.data))
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        return {"columns": df.columns.tolist(), "dtypes": dtypes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")
