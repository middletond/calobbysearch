#!/usr/bin/env bash

# Deploy Django / Postgres app.
echo "Migrating django models to database."
python3 manage.py migrate

echo "Restarting Nginx."
sudo service nginx restart
