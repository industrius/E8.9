import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_word_parse.settings")

app = Celery("web_word_parse")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()