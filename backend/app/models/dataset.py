from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    # NEW: store the file path or S3 key
    storage_key = Column(String, nullable=True)  

    # NEW: flag to indicate if stored in S3 or locally
    is_s3 = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="datasets")
    files = relationship("DatasetFile", back_populates="dataset")
    experiments = relationship("Experiment", back_populates="dataset")
