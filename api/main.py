from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
import json

app = FastAPI(title="Fargate Async File Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



STORAGE_DIR = Path("storage")
UPLOAD_DIR = STORAGE_DIR / "uploads"
QUEUE_FILE = STORAGE_DIR / "queue.jsonl"
JOBS_FILE = STORAGE_DIR / "jobs.json"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

if not JOBS_FILE.exists():
    JOBS_FILE.write_text("[]")


def load_jobs():
    with JOBS_FILE.open("r") as f:
        return json.load(f)


def save_jobs(jobs):
    with JOBS_FILE.open("w") as f:
        json.dump(jobs, f, indent=2)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    message = {
        "job_id": job_id,
        "filename": file.filename,
        "file_path": str(file_path),
        "status": "pending",
    }

    jobs = load_jobs()
    jobs.append({
        "job_id": job_id,
        "filename": file.filename,
        "status": "pending",
        "result_path": None
    })
    save_jobs(jobs)

    with QUEUE_FILE.open("a") as queue:
        queue.write(json.dumps(message) + "\n")

    return {
        "job_id": job_id,
        "message": "File uploaded successfully and queued for processing",
    }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    jobs = load_jobs()

    for job in jobs:
        if job["job_id"] == job_id:
            return job

    raise HTTPException(status_code=404, detail="Job not found")


@app.get("/jobs/{job_id}/result")
def get_job_result(job_id: str):
    processed_file = STORAGE_DIR / "processed" / f"{job_id}.json"

    if not processed_file.exists():
        raise HTTPException(status_code=404, detail="Result not found")

    with processed_file.open("r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/jobs/{job_id}/download")
def download_result(job_id: str):
    file_path = STORAGE_DIR / "processed" / f"{job_id}.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=f"{job_id}.json",
        media_type="application/json"
    )

    file_path = STORAGE_DIR / "processed" / f"{job_id}.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=f"{job_id}.json",
        media_type="application/json"
    )
