from pathlib import Path
from backend_factory import get_storage_backend, get_queue_backend
import csv
import json
import time

STORAGE_DIR = Path("storage")
JOBS_FILE = STORAGE_DIR / "jobs.json"

storage = get_storage_backend()
queue = get_queue_backend()

def process_csv_to_json(file_path: Path, output_path: Path):
    with file_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2)


def update_job_status(job_id: str, status: str, result_path: str | None = None):
    if not JOBS_FILE.exists():
        return

    with JOBS_FILE.open("r") as f:
        jobs = json.load(f)

    for job in jobs:
        if job["job_id"] == job_id:
            job["status"] = status
            job["result_path"] = result_path

    with JOBS_FILE.open("w") as f:
        json.dump(jobs, f, indent=2)


def main():
    print("Worker started...")

    while True:
        jobs = queue.dequeue_jobs()

        for job in jobs:
            file_path = Path(job["file_path"])
            job_id = job["job_id"]

            if file_path.exists():
                output_path = storage.get_processed_file_path(job_id)

                process_csv_to_json(file_path, output_path)

                update_job_status(
                    job_id,
                    "completed",
                    str(output_path)
                )

                print(f"Processed job {job_id}")

            else:
                update_job_status(job_id, "failed")
                print(f"File not found for job {job_id}")

        time.sleep(5)


if __name__ == "__main__":
    main()
