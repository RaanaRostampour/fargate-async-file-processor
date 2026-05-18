from config import STORAGE_BACKEND, QUEUE_BACKEND


def get_storage_backend():
    if STORAGE_BACKEND == "local":
        from storage_backend import local_storage
        return local_storage

    if STORAGE_BACKEND == "s3":
        from storage_backend import s3_storage
        return s3_storage

    raise ValueError(f"Unsupported storage backend: {STORAGE_BACKEND}")


def get_queue_backend():
    if QUEUE_BACKEND == "local":
        from queue_backend import local_queue
        return local_queue

    if QUEUE_BACKEND == "sqs":
        from queue_backend import sqs_queue
        return sqs_queue

    raise ValueError(f"Unsupported queue backend: {QUEUE_BACKEND}")
