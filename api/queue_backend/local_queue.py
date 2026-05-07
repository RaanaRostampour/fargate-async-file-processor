from pathlib import Path
import json

QUEUE_FILE = Path("storage/queue.jsonl")


def enqueue(message):
    with QUEUE_FILE.open("a") as queue:
        queue.write(json.dumps(message) + "\n")


def dequeue_jobs():
    if not QUEUE_FILE.exists():
        return []

    with QUEUE_FILE.open("r") as queue:
        jobs = [json.loads(line) for line in queue if line.strip()]

    QUEUE_FILE.write_text("")

    return jobs
