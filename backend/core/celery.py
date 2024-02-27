
from celery import Celery




celery_app = Celery(
    __name__,
    backend="redis://127.0.0.1:6379",
    broker="redis://127.0.0.1:6379",
    include= ["api.celery_task"])

celery_app.autodiscover_tasks(related_name='celery_task')
# celery_app.task_routes = {'api.celery_task.send_email_task': {'queue': 'send'}}
# celery_app.task_routes = {
#     'api.celery_task.send_email_task': 'default',
# }