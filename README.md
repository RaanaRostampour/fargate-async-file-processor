# Fargate Async File Processor

A cloud-native, event-driven file processing pipeline built on AWS.
This project demonstrates how to design and deploy a scalable async system using containerized services on AWS Fargate.

---

## Overview

This system allows users to upload files (e.g., CSV), processes them asynchronously, and stores the results (e.g., JSON) back in cloud storage.

It follows an event-driven architecture and separates responsibilities between API and worker services for better scalability and reliability.

---

## Architecture

User → API (FastAPI)
↓
Upload to S3
↓
Send message to SQS
↓
Worker (Fargate)
↓
Process file (CSV → JSON)
↓
Store result in S3

---

## Tech Stack

* Backend API: FastAPI (Python)
* Worker Service: Python
* Containerization: Docker
* Compute: AWS Fargate (ECS)
* Storage: Amazon S3
* Queue: Amazon SQS
* Monitoring: AWS CloudWatch
* Infrastructure (optional): Terraform or CloudFormation

---

## Features

* File upload via REST API
* Asynchronous background processing
* Event-driven architecture using message queues
* Scalable worker services with AWS Fargate
* Fault-tolerant design
* Clear separation between API and processing layer

---

## Project Structure

fargate-async-file-processor/
├── api/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── worker/
│   ├── worker.py
│   ├── requirements.txt
│   └── Dockerfile
├── infra/
│   └── terraform/
├── docker-compose.yml
└── README.md

---

## How It Works

1. User uploads a file via the API
2. API stores the file in S3
3. API sends a message to SQS with file metadata
4. Worker service polls SQS
5. Worker downloads the file from S3
6. Worker processes the file (CSV to JSON)
7. Processed output is uploaded back to S3

---

## Local Development

### Prerequisites

* Docker and Docker Compose
* Python 3.10 or higher

### Run locally

```bash
docker-compose up --build
```

---

## Deployment (AWS)

High-level steps:

1. Build Docker images
2. Push images to Amazon ECR
3. Create ECS cluster with Fargate
4. Configure S3 bucket
5. Create SQS queue
6. Deploy API and Worker services
7. Configure IAM roles and permissions

---

## IAM Permissions (Simplified)

* S3: read and write access
* SQS: send, receive, and delete messages
* CloudWatch: logging

---

## Future Improvements

* Add authentication (JWT)
* Add database for job tracking (PostgreSQL or DynamoDB)
* Implement retry mechanism and dead-letter queue
* Add CI/CD pipeline (GitHub Actions or GitLab CI)
* Add monitoring dashboard (Prometheus and Grafana)

---

## Example

Input CSV:

```json
name,age
Ali,25
Sara,30
```

Output JSON:

```json
[
  {"name": "Ali", "age": 25},
  {"name": "Sara", "age": 30}
]
```

---

## Learning Outcomes

* Designing event-driven systems
* Working with AWS Fargate and ECS
* Building scalable async pipelines
* Container-based deployment
* Cloud architecture best practices

---

## License

MIT License

