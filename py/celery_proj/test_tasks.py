from __future__ import absolute_import
import time

from celery_proj.celery import app

@app.task
def add(x, y):
    time.sleep(20)
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
