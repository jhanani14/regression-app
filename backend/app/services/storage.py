import boto3
import uuid
from app.core.config import settings
from io import BytesIO

# Initialize S3 client
s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def make_key(user_id: int, filename: str) -> str:
    """
    Generate a unique key for storing the file in S3
    """
    ext = filename.split(".")[-1] if "." in filename else ""
    return f"{user_id}/{uuid.uuid4().hex}.{ext}"


def upload_fileobj(fileobj: BytesIO, key: str, content_type: str = None) -> str:
    """
    Upload a file-like object to S3
    """
    try:
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        s3.upload_fileobj(fileobj, settings.S3_BUCKET, key, ExtraArgs=extra_args)
        return key
    except Exception as e:
        print("❌ Error while uploading to S3:", e)
        raise


def download_to_bytes(key: str) -> bytes:
    """
    Download a file from S3 as bytes
    """
    obj = s3.get_object(Bucket=settings.S3_BUCKET, Key=key)
    return obj["Body"].read()
