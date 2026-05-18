resource "aws_s3_bucket" "files" {
bucket = "${var.project_name}-storage-raana"

  tags = {
    Project = var.project_name
  }
}

resource "aws_sqs_queue" "jobs" {
  name = "${var.project_name}-jobs"

  tags = {
    Project = var.project_name
  }
}
