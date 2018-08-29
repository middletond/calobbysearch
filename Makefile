celery:
	celery -A service worker -l info -c 5
celery-debug:
	celery -A service worker -l debug -c 1
celery-background:
	screen -dmS celery sh
	sleep 1
	screen -S celery -p 0 -X stuff "make celery\n"
	echo "Connect to celery feed with 'screen -r celery'"
redis:
	redis-server
redis-background:
	screen -dmS redis sh
	sleep 1
	screen -S redis -p 0 -X stuff "make redis\n"
	echo "Connect to redis feed with 'screen -r redis"

uwsgi:
	uwsgi --socket 127.0.0.1:8080 --module service.wsgi:application
uwsgi-background:
	screen -dmS uwsgi sh
	sleep 1
	screen -S uwsgi -p 0 -X stuff "make uwsgi\n"
	echo "Connect to uwsgi server feed with 'screen -r uwsgi"
serve:
	python manage.py runserver
