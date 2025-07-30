import os
from celery import Celery
import ssl
from dotenv import load_dotenv
load_dotenv()
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webN.settings')

app = Celery('webN')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE  # or CERT_REQUIRED
}
app.autodiscover_tasks()