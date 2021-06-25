from celery import Celery
from flask_redis import FlaskRedis

celery = Celery("webhook-processor")
redis_client = FlaskRedis()
