# backend/routers/results.py
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ✅ Refactored imports
from app.deps import get_db
from app.models.experiment import Experiment

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{experiment_id}/download")
def download_results(experiment_id: int, db: Session = Depends(get_db)):
    """
    Generate a PDF report for the experiment and return as a download.
    """
    # Fetch experiment from DB
    exp = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # PDF path
    pdf_path = f"results_{experiment_id}.pdf"
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"Experiment {experiment_id}", styles["Title"]))
    story.append(Spacer(1, 12))

    # Add metrics
    # exp.metrics is a list of ExperimentMetric objects
    for metric in getattr(exp, "metrics", []):
        story.append(Paragraph(f"{metric.metric_name}: {metric.metric_value}", styles["Normal"]))
        story.append(Spacer(1, 6))

    # Add plot if exists
    plot_path = f"plot_{experiment_id}.png"
    if os.path.exists(plot_path):
        story.append(Image(plot_path, width=400, height=300))

    # Build PDF
    doc.build(story)

    return FileResponse(pdf_path, filename=f"experiment_{experiment_id}.pdf")
