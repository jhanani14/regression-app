# backend/app/services/storage_local.py
from pathlib import Path
import shutil
import uuid

# Folder where local files will be stored
LOCAL_DIR = Path("backend_local_storage")
LOCAL_DIR.mkdir(exist_ok=True)

def make_key(user_id: int, filename: str) -> str:
    """Generate a unique filename for each user"""
    ext = filename.split(".")[-1] if "." in filename else ""
    return f"{user_id}_{uuid.uuid4().hex}.{ext}"

def upload_fileobj(fileobj, key: str, content_type: str = None) -> str:
    """
    Save uploaded file locally.
    (content_type is ignored here to stay compatible with S3 version)
    """
    dest_path = LOCAL_DIR / key
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(fileobj, f)
    return key

def download_to_bytes(key: str) -> bytes:
    """Read file from local storage"""
    path = LOCAL_DIR / key
    with open(path, "rb") as f:
        return f.read()
