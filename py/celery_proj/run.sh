exit
celery -A celery_proj worker -l info

celery multi start w1 -A celery_proj -l info
celery multi restart w1 -A celery_proj -l info
celery multi stop w1 -A celery_proj -l info
celery multi stopwait w1 -A celery_proj -l info

--pidfile=/var/run/celery/%n.pid
--logfile=/var/log/celery/%n%I.log

 
celery multi start w1 -A celery_proj -l info --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
celery multi stop w1 -A celery_proj -l info --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
