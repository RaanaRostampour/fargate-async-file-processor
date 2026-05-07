from config import STORAGE_BACKEND, QUEUE_BACKEND

from storage_backend import local_storage
from queue_backend import local_queue


def get_storage_backend():
    if STORAGE_BACKEND == "local":
        return local_storage

    raise ValueError(f"Unsupported storage backend: {STORAGE_BACKEND}")


def get_queue_backend():
    if QUEUE_BACKEND == "local":
        return local_queue

    raise ValueError(f"Unsupported queue backend: {QUEUE_BACKEND}")
