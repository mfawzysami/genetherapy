from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from genetherapy.settings import CELERY_DEFAULT_QUEUE , CELERY_DEFAULT_EXCHANGE , CELERY_DEFAULT_ROUTING_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE','genetherapy.settings')
app = Celery('genetherapy')
app.conf.task_default_queue = CELERY_DEFAULT_QUEUE
app.conf.task_default_exchange = CELERY_DEFAULT_EXCHANGE
app.conf.task_default_routing_key = CELERY_DEFAULT_ROUTING_KEY
app.config_from_object('django.conf.settings',namespace='CELERY')
app.autodiscover_tasks()