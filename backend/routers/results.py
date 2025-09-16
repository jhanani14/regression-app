# backend/routers/results.py
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from backend.db import SessionLocal
from backend.models import Experiment  # assuming you have this model

router = APIRouter(prefix="/results", tags=["results"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{experiment_id}/download")
def download_results(experiment_id: int, db: Session = Depends(get_db)):
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    pdf_path = f"results_{experiment_id}.pdf"
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Experiment {experiment_id}", styles["Title"]))
    story.append(Spacer(1, 12))

    # Add metrics
    if isinstance(exp.metrics, dict):
        for key, val in exp.metrics.items():
            story.append(Paragraph(f"{key}: {val}", styles["Normal"]))
            story.append(Spacer(1, 6))

    # Add plot if available
    plot_path = f"plot_{experiment_id}.png"
    if os.path.exists(plot_path):
        story.append(Image(plot_path, width=400, height=300))

    doc.build(story)

    return FileResponse(pdf_path, filename=f"experiment_{experiment_id}.pdf")
