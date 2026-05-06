output "bucket_name" {
  value = aws_s3_bucket.files.bucket
}

output "queue_url" {
  value = aws_sqs_queue.jobs.url
}
