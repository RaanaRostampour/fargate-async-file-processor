import boto3
import os
import json

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")


def enqueue(message):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )


def dequeue_jobs():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=1
    )

    messages = response.get("Messages", [])

    jobs = []

    for msg in messages:
        jobs.append(json.loads(msg["Body"]))

        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg["ReceiptHandle"]
        )

    return jobs
