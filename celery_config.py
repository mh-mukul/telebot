import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST=os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT=int(os.environ.get("REDIS_PORT", 6379))
REDIS_CELERY_BROKER_DB=int(os.environ.get("REDIS_CELERY_BROKER_DB", 0))
REDIS_CELERY_BACKEND_DB=int(os.environ.get("REDIS_CELERY_BACKEND_DB", 0))


celery_app = Celery(
    "telebot",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BROKER_DB}",  # Redis broker URL
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BACKEND_DB}",  # Redis backend URL (optional)
    broker_connection_retry_on_startup=True,
)


# Function to import tasks after app initialization
def register_tasks():
    import tasks


register_tasks()
