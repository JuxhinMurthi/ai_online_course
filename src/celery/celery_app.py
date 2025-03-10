import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
celery_app = Celery("src", broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)
