from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_manager.settings')

app = Celery('budget_manager')

# Load settings from Django settings, using a 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered Django app configs
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')