#!/usr/bin/env bash
SITE_ROOT="/var/www/lobbysearch"
START_SCRIPT=$SITE_ROOT"/deploy/restart.sh"

cd $SITE_ROOT

# Deploy Django / Postgres app.
echo "Migrating django models to database."
source venv/bin/activate
python3 manage.py migrate

echo "Starting all services."
source $START_SCRIPT
