import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_CELERY_BROKER_DB = int(os.environ.get("REDIS_CELERY_BROKER_DB", 0))
REDIS_CELERY_BACKEND_DB = int(os.environ.get("REDIS_CELERY_BACKEND_DB", 0))


celery_app = Celery(
    "telebot",
    # Redis broker URL
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BROKER_DB}",
    # Redis backend URL (optional)
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BACKEND_DB}",
    broker_connection_retry_on_startup=True,
)

# Ensure unique queue name
celery_app.conf.task_default_queue = 'telebot-queue'

# Optional: Prefix task results with a namespace
celery_app.conf.redis_backend_health_check_interval = 30
celery_app.conf.result_backend_transport_options = {
    'prefix': 'telebot-results:',
    'visibility_timeout': 3600
}


# Function to import tasks after app initialization
def register_tasks():
    import tasks


register_tasks()
