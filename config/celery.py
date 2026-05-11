import os
from celery import Celery

# Sets up Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery ("portfolioiq")

# Read Celery config from Django settings, looking for CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-find tasks.py files in all installed apps
app.autodiscover_tasks()