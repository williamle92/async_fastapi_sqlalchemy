from celery import Celery

app = Celery("hyperion", broker="redis://localhost")


@app.task
def add(x, y):
    return x + y
