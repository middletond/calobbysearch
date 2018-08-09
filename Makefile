celery:
	celery -A service worker -l info -c 8
celery-debug:
	celery -A service worker -l debug -c 1
celery-background:
	screen -dmS celery sh
	sleep 1
	screen -S celery -p 0 -X stuff "make celery\n"
	echo "Connect to celery feed with 'screen -r celery"
uwsgi:
	uwsgi --socket 127.0.0.1:8000 --module service.wsgi:application
serve:
	python manage.py runserver
