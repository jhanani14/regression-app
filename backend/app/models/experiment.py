from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    target = Column(String, nullable=True)
    features = Column(Text, nullable=True)     # store comma-separated list
    algorithm = Column(String, nullable=True)
    status = Column(String, default="done")

    dataset = relationship("Dataset", back_populates="experiments")
    metrics = relationship("ExperimentMetric", back_populates="experiment")
    artifacts = relationship("ExperimentArtifact", back_populates="experiment")


class ExperimentMetric(Base):
    __tablename__ = "experiment_metrics"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)

    experiment = relationship("Experiment", back_populates="metrics")


class ExperimentArtifact(Base):
    __tablename__ = "experiment_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    artifact_path = Column(String, nullable=False)
    data = Column(LargeBinary)

    experiment = relationship("Experiment", back_populates="artifacts")
