import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.leetcode_analogue_backend.settings')

app = Celery('leetcode_analogue_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
