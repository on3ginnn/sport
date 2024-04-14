import os

import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
app = celery.Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
