celery:
	celery -A service worker -l info -c 8
celery-debug:
	celery -A service worker -l debug -c 1
celery-background:
	screen -dmS celery sh
	sleep 1
	screen -S celery -p 0 -X stuff "make celery\n"
	echo "Connect to celery feed with 'screen -r celery"

redis:
	redis-server
redis-background:
	screen -dmS redis sh
	sleep 1
	screen -S redis -p 0 -X stuff "make redis\n"
	echo "Connect to redis feed with 'screen -r redis"

serve:
	uwsgi --socket 127.0.0.1:8080 --module service.wsgi:application
serve-background:
	screen -dmS server sh
	sleep 1
	screen -S server -p 0 -X stuff "make serve\n"
	echo "Connect to uwsgi server feed with 'screen -r server"
serve-dev:
	python manage.py runserver
