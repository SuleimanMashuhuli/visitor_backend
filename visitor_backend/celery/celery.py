import os
from celery import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visitor_backend.settings')

app = celery('visitor_backend')
app.config_from_object('django.config:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')