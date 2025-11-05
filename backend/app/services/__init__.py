from app.core.config import settings

# Decide automatically based on your .env flag
if settings.USE_S3:
    from app.services import storage as storage_adapter
else:
    from app.services import storage_local as storage_adapter
