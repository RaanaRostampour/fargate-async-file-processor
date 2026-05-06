from pathlib import Path
import csv
import json
import time

STORAGE_DIR = Path("storage")
QUEUE_FILE = STORAGE_DIR / "queue.jsonl"
JOBS_FILE = STORAGE_DIR / "jobs.json"
PROCESSED_DIR = STORAGE_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def process_csv_to_json(file_path: Path, job_id: str):
    output_path = PROCESSED_DIR / f"{job_id}.json"

    with file_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2)

    print(f"Processed job {job_id}: {output_path}")


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


def read_jobs():
    if not QUEUE_FILE.exists():
        return []

    with QUEUE_FILE.open("r") as queue:
        return [json.loads(line) for line in queue if line.strip()]


def clear_queue():
    QUEUE_FILE.write_text("")


def main():
    print("Worker started...")

    while True:
        jobs = read_jobs()

        if jobs:
            clear_queue()

            for job in jobs:
                file_path = Path(job["file_path"])
                job_id = job["job_id"]

                if file_path.exists():
                    process_csv_to_json(file_path, job_id)

                    result_path = str(PROCESSED_DIR / f"{job_id}.json")
                    update_job_status(job_id, "completed", result_path)
                else:
                    print(f"File not found for job {job_id}")
                    update_job_status(job_id, "failed")

        time.sleep(5)


if __name__ == "__main__":
    main()
