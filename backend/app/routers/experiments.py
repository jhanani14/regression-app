from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
# Lazy-load pandas to avoid segfault issues in Docker Desktop Mac
# pandas will only be imported when actually needed
import io, base64, os
from jose import jwt, JWTError
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import math

# ✅ Imports from your app
from app.deps import get_db, get_current_user
from app.models.experiment import Experiment, ExperimentMetric, ExperimentArtifact
from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.services.ml_pipeline import train_pipeline
from app.services.classification import CLASSIFICATION_ALGORITHMS
from app.services.regression import REGRESSION_ALGORITHMS
# Temporarily disable matplotlib plots due to Docker Desktop Mac threading issues
# from app.services.plots import (
#     residual_plot,
#     predicted_vs_actual,
#     confusion_matrix_plot,
#     roc_curve_plot,
# )

# Placeholder functions that return None (no plots)
def residual_plot(y_true, y_pred):
    return None
def predicted_vs_actual(y_true, y_pred):
    return None
def confusion_matrix_plot(y_true, y_pred):
    return None
def roc_curve_plot(model, X_test, y_test):
    return None
from app.services import storage  # ✅ Use your unified storage handler

router = APIRouter(prefix="/experiments", tags=["experiments"])

# ============================
# Helper to clean metrics
# ============================
def clean_metrics(metrics: dict):
    """Replace NaN or Inf values with 0.0 for JSON serialization."""
    return {k: (0.0 if (v is None or math.isnan(v) or math.isinf(v)) else v) for k, v in metrics.items()}

# ============================
# Algorithm Info
# ============================
@router.get("/algorithm-info")
def get_algorithm_info():
    """Return algorithm descriptions for frontend."""
    # Return only metadata, not the actual model instances
    def get_algorithm_metadata(algorithms):
        result = {}
        for key, value in algorithms.items():
            result[key] = {
                "type": value["type"],
                "description": value["description"],
                "best_for": value["best_for"],
                # Don't include the model instance
            }
        return result
    
    return {
        "classification_algorithms": get_algorithm_metadata(CLASSIFICATION_ALGORITHMS),
        "regression_algorithms": get_algorithm_metadata(REGRESSION_ALGORITHMS),
    }

# ============================
# Schemas
# ============================
class RunRequest(BaseModel):
    dataset_id: int
    target: str
    features: list[str] = []
    split: float = 0.2
    algorithm: str = "linear_regression"

# ============================
# Run Experiment
# ============================
@router.post("/run")
def run_experiment(
    req: RunRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    dataset = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset_file = db.query(DatasetFile).filter(DatasetFile.dataset_id == dataset.id).first()
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset file not found")

    try:
        file_bytes = storage.download_to_bytes(dataset_file.s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")

    try:
        import pandas as pd  # Lazy-load pandas
        if dataset_file.s3_key.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    if req.target not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target '{req.target}' not found in dataset")

    pipeline, metrics, X_test, y_test, preds = train_pipeline(
        df, req.target, test_size=req.split, algorithm=req.algorithm
    )

    exp = Experiment(
        dataset_id=dataset.id,
        created_at=datetime.utcnow(),
        target=req.target,
        features=",".join(req.features) if req.features else None,
        algorithm=req.algorithm,
        status="done",
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)

    for k, v in metrics.items():
        db.add(
            ExperimentMetric(experiment_id=exp.id, metric_name=k, metric_value=float(v))
        )

    # Temporarily disabled plots due to Docker threading issues
    # Plots will return None and won't be saved
    if any(x in req.algorithm for x in ["classifier", "logistic", "svm", "knn"]):
        cm_plot = confusion_matrix_plot(y_test, preds)
        if cm_plot:  # Only add if plot was generated
            db.add(
                ExperimentArtifact(
                    experiment_id=exp.id, artifact_path="confusion_matrix.png", data=cm_plot
                )
            )
        roc_plot = roc_curve_plot(pipeline, X_test, y_test)
        if roc_plot:
            db.add(
                ExperimentArtifact(
                    experiment_id=exp.id, artifact_path="roc_curve.png", data=roc_plot
                )
            )
    else:
        res_plot = residual_plot(y_test, preds)
        if res_plot:  # Only add if plot was generated
            db.add(
                ExperimentArtifact(
                    experiment_id=exp.id, artifact_path="residual_plot.png", data=res_plot
                )
            )
        pva_plot = predicted_vs_actual(y_test, preds)
        if pva_plot:  # Only add if plot was generated
            db.add(
                ExperimentArtifact(
                    experiment_id=exp.id,
                    artifact_path="predicted_vs_actual.png",
                    data=pva_plot,
                )
            )

    db.commit()
    return {"experiment_id": exp.id}

# ============================
# Get Experiment
# ============================
@router.get("/{experiment_id}")
def get_experiment(
    experiment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    metrics = {m.metric_name: m.metric_value for m in exp.metrics}
    metrics = clean_metrics(metrics)  # ✅ Clean NaN/Inf values
    plots = [base64.b64encode(a.data).decode("utf-8") for a in exp.artifacts]

    return {
        "id": exp.id,
        "created_at": exp.created_at.isoformat(),
        "target": exp.target,
        "features": exp.features.split(",") if exp.features else [],
        "algorithm": exp.algorithm,
        "status": exp.status,
        "metrics": metrics,
        "plots": plots,
    }

# ============================
# List Experiments
# ============================
@router.get("")
def list_experiments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    exps = db.query(Experiment).order_by(Experiment.created_at.desc()).all()
    return [
        {
            "id": e.id,
            "created_at": e.created_at.isoformat(),
            "target": e.target,
            "status": e.status,
            "metrics": clean_metrics({m.metric_name: m.metric_value for m in e.metrics}),
        }
        for e in exps
    ]

# ============================
# Download Experiment as PDF
# ============================
@router.get("/{experiment_id}/download")
def download_experiment_pdf(
    experiment_id: int,
    token: str = Query(None),
    db: Session = Depends(get_db),
):
    if token:
        try:
            jwt.decode(token, os.getenv("JWT_SECRET", "change-me"), algorithms=["HS256"])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        get_current_user()

    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    metrics = clean_metrics({m.metric_name: m.metric_value for m in exp.metrics})
    plots = [a.data for a in exp.artifacts]

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Experiment Report - ID {exp.id}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Algorithm: {exp.algorithm}")
    c.drawString(50, height - 100, f"Target: {exp.target}")
    c.drawString(
        50, height - 120, f"Created At: {exp.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 160, "Metrics:")
    c.setFont("Helvetica", 12)
    y = height - 180
    for k, v in metrics.items():
        c.drawString(70, y, f"{k}: {v:.4f}")
        y -= 20

    y -= 40
    for plot_bytes in plots:
        img = ImageReader(io.BytesIO(plot_bytes))
        img_height = 200
        if y - img_height < 50:
            c.showPage()
            y = height - 50
        c.drawImage(
            img,
            50,
            y - img_height,
            width=500,
            height=img_height,
            preserveAspectRatio=True,
            mask="auto",
        )
        y -= img_height + 40

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=experiment_{exp.id}.pdf"},
    )
