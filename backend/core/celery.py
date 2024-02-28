
from celery import Celery

from core.config import settings


celery_app = Celery(
    __name__,
    backend=settings.REDIS_URL,
    broker=settings.REDIS_URL,
    include= ["api.celery_task"])

celery_app.autodiscover_tasks(related_name='celery_task')
# celery_app.task_routes = {'api.celery_task.send_email_task': {'queue': 'send'}}
# celery_app.task_routes = {
#     'api.celery_task.send_email_task': 'default',
# }