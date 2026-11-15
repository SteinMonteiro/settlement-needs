import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settlement_needs.settings')

app = Celery('settlement_needs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
