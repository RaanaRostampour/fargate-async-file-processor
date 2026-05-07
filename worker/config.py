import os

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
QUEUE_BACKEND = os.getenv("QUEUE_BACKEND", "local")
