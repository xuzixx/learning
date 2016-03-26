from celery import Celery

app = Celery("my_celery")
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y
