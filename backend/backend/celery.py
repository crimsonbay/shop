from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue
from backend import settings
# Основыне настройки Django для celery
# The main Django settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('high', Exchange('high'), routing_key='high'),
    Queue('normal', Exchange('normal'), routing_key='normal'),
    Queue('low', Exchange('low'), routing_key='low'),
)

app.conf.task_default_queue = 'normal'
app.conf.task_default_exchange = 'normal'
app.conf.task_default_routing_key = 'normal'


# task_routes = {
#     -- HIGH PRIORITY QUEUE -- #
#     'myapp.tasks.check_payment_status': {'queue': 'high'},
#     -- LOW PRIORITY QUEUE -- #
#     'myapp.tasks.close_session': {'queue': 'low'},
# }
