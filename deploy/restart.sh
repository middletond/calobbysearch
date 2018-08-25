#!/usr/bin/env bash

#SITE_ROOT="$( cd "$( dirname "${BASH_SOURCE[1]}" )" && pwd )"
SITE_ROOT="/var/www/lobbysearch"

source venv/bin/activate

echo "Stopping all app services..."
sudo service nginx stop
sudo killall screen # kills celery + uwsgi
sudo killall redis-server # redis will keep running despite killing screen

echo "Restarting app internal services..."

echo "Restarting celery."
make celery-background

echo "Restarting redis."
make redis-background

echo "Restarting app web servers..."

echo "Restarting uwsgi."
make uwsgi-background

echo "Restarting nginx."
sudo service nginx start

echo "Done. The following services are running on screens:"
sudo screen -ls
