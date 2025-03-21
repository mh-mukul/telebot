import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


celery_app = Celery(
    "telebot",
    broker=CELERY_BROKER_URL,  # Redis broker URL
    backend=CELERY_RESULT_BACKEND,  # Redis backend URL (optional)
    broker_connection_retry_on_startup=True,
)


# Function to import tasks after app initialization
def register_tasks():
    import tasks


register_tasks()
