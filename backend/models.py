from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, LargeBinary, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    datasets = relationship("Dataset", back_populates="user")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="datasets")
    files = relationship("DatasetFile", back_populates="dataset")
    experiments = relationship("Experiment", back_populates="dataset")


class DatasetFile(Base):
    __tablename__ = "dataset_files"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    filename = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)

    dataset = relationship("Dataset", back_populates="files")


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ extra fields for frontend
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
