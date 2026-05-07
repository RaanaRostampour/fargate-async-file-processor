from pathlib import Path
import shutil

STORAGE_DIR = Path("storage")
UPLOAD_DIR = STORAGE_DIR / "uploads"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(upload_file, destination):
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

PROCESSED_DIR = STORAGE_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_processed_file_path(job_id):
    return PROCESSED_DIR / f"{job_id}.json"
