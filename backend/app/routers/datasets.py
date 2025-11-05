from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
from io import BytesIO

from app.deps import get_db, get_current_user
from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.services import storage  # ✅ storage.py handler

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload")
async def upload_dataset(
    file: UploadFile,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Upload CSV/XLSX file, store it in S3/local storage, and return dataset_id + columns.
    """
    try:
        # Read file into bytes
        file_bytes = await file.read()

        # Detect supported file type
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(file_bytes))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(file_bytes))
        else:
            raise HTTPException(status_code=400, detail="Only CSV/XLSX supported")

        # Create dataset entry
        dataset = Dataset(
            name=file.filename,
            user_id=user.id,
            uploaded_at=datetime.utcnow()
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        # Generate storage key (unique path)
        key = storage.make_key(user.id, file.filename)

        # Upload file to chosen storage (S3/local)
        storage.upload_fileobj(BytesIO(file_bytes), key, content_type=file.content_type)

        # Save file metadata to DB
        dataset_file = DatasetFile(
            dataset_id=dataset.id,
            filename=file.filename,
            s3_key=key,
            content_type=file.content_type,
            size=len(file_bytes)
        )
        db.add(dataset_file)
        db.commit()

        return {
            "dataset_id": dataset.id,
            "name": dataset.name,
            "columns": df.columns.tolist()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{dataset_id}/columns")
def get_columns(
    dataset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Fetch dataset file from storage and return its columns.
    """
    dataset_file = db.query(DatasetFile).filter(DatasetFile.dataset_id == dataset_id).first()
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        if dataset_file.s3_key:
            data = storage.download_to_bytes(dataset_file.s3_key)
        else:
            data = dataset_file.data  # fallback for legacy storage

        # Auto-detect CSV or XLSX
        if dataset_file.s3_key.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(data))
        else:
            df = pd.read_csv(BytesIO(data))

        return {"columns": df.columns.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")


@router.get("/{dataset_id}/info")
def get_dataset_info(
    dataset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Return both columns and their data types.
    """
    dataset_file = db.query(DatasetFile).filter(DatasetFile.dataset_id == dataset_id).first()
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        if dataset_file.s3_key:
            data = storage.download_to_bytes(dataset_file.s3_key)
        else:
            data = dataset_file.data

        # Auto-detect CSV/XLSX
        if dataset_file.s3_key.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(data))
        else:
            df = pd.read_csv(BytesIO(data))

        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        return {"columns": df.columns.tolist(), "dtypes": dtypes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")
