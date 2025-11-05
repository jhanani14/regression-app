from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.session import Base

class DatasetFile(Base):
    __tablename__ = "dataset_files"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    filename = Column(String, nullable=False)

    # ✅ Current fields for S3/local storage
    s3_key = Column(String, nullable=True)         # path/key in S3 or local storage
    content_type = Column(String, nullable=True)   # MIME type (e.g. text/csv)
    size = Column(BigInteger, nullable=True)       # file size in bytes

    # ❌ Removed old binary field (data)

    dataset = relationship("Dataset", back_populates="files")
