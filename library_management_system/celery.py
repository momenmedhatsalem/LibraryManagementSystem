import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')

celery_app = Celery('library_management_system')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
