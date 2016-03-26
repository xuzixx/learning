from __future__ import absolute_import

from celery import Celery

#app = Celery('proj',
#        broker='redis://:wxtest@localhost:6379/0',
#        backend='redis://:wxtest@localhost:6379/0',
#        include=['proj.my_tasks'])
app = Celery('proj', include = ["celery_proj.test_tasks"])
app.config_from_object('celery_proj.celeryconfig')

if __name__ == '__main__':
    app.start()


