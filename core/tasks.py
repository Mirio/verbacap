import os
from os.path import getsize, join

from celery import Celery
from django.conf import settings

from core.models import Settings
from core.shared import CommonResponse

app = Celery("tasks")


@app.task
def calcolate_persistinfo() -> CommonResponse:
    out = CommonResponse()
    total_bytessize = 0
    total_counter = 0
    for root, _, files in os.walk(settings.PERSIST_AUDIO_ROOTDIR):
        for fname in files:
            total_bytessize += getsize(join(root, fname))
            total_counter += 1
    Settings.objects.get_or_create(name="persist_total_size", value=total_bytessize)
    Settings.objects.get_or_create(name="persist_total_count", value=total_counter)
    out.status = "success"
    return out.__dict__
