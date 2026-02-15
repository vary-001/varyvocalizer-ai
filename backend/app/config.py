import os
from pathlib import Path

class Settings:
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Where uploaded files go
    UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
    
    # Where Demucs outputs the stems
    RESULTS_DIR = os.path.join(BASE_DIR, "storage", "separated")
    
    # Redis URL (Service name in docker-compose is 'redis')
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)