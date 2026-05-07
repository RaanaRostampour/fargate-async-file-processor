# Async File Processor (Local Version)

A simple backend system that processes CSV files asynchronously.

---

## What This Project Does

* You upload a CSV file
* The system saves it locally
* A background worker processes it
* The result (JSON) is saved
* You can check status or download the result

---

## How It Works

```text
User uploads file
        ↓
API creates processing job
        ↓
Storage backend saves file
        ↓
Queue backend stores job
        ↓
Worker reads queued jobs
        ↓
Worker converts CSV → JSON
        ↓
Processed result is saved

---

## Why This Exists

This project is a simple example of:

* separating API from background processing
* building a basic job queue
* designing async workflows

---

## Current Architecture

The project uses a simple backend abstraction layer.

This makes it possible to switch infrastructure implementations later:

- local storage → AWS S3
- local queue → AWS SQS

without rewriting the application logic.
---

## API Endpoints

### Upload

POST /upload

Returns:

```json
{
  "job_id": "..."
}
```

---

### Check Status

GET /jobs/{job_id}

---

### Get Result

GET /jobs/{job_id}/result

---

### Download Result

GET /jobs/{job_id}/download

---

## Run Locally

### Start backend

```bash
docker compose up --build
```

---

### Start frontend

```bash
cd frontend
python3 -m http.server 3000
```

Open:

```text
http://localhost:3000
```

---

## Project Structure

```text
api/        → handles upload and API
worker/     → processes files
storage/    → local files (uploads + results)
frontend/   → simple UI
```

---

## Important Note

This is a **local prototype**.

* Queue = file (not SQS)
* Storage = local folder (not S3)

---

## Next Steps (Planned)

* Replace storage with AWS S3
* Replace queue with AWS SQS
* Deploy on AWS Fargate
