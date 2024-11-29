from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django'nun settings modülünü Celery'ye bildirin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracker.settings')

# Celery uygulamasını başlat
app = Celery('Tracker')

# Django'nun settings.py dosyasındaki tüm Celery ayarlarını yükle
app.config_from_object('django.conf:settings', namespace='CELERY')

# Görevleri (tasks) otomatik olarak keşfet
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
