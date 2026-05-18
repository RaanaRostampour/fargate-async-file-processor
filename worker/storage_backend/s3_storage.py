import boto3
import os
from pathlib import Path

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET")


def save_uploaded_file(upload_file, destination):
    temp_path = Path("/tmp") / destination.name

    with temp_path.open("wb") as buffer:
        buffer.write(upload_file.file.read())

    s3.upload_file(
        str(temp_path),
        BUCKET_NAME,
        f"uploads/{destination.name}"
    )


def get_processed_file_path(job_id):
    return f"s3://{BUCKET_NAME}/processed/{job_id}.json"
