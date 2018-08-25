#!/usr/bin/env bash

# Setup Django / Postgres environment on Ubuntu 16.04

#SITE_ROOT="$( cd "$( dirname "${BASH_SOURCE[1]}" )" && pwd )"
SITE_ROOT="/var/www/lobbysearch"

SERVER_CONF_SOURCE=$SITE_ROOT"/deploy/server.conf"
SERVER_CONF_DEST="/etc/nginx/sites-enabled/default"

NGINX_CONF_SOURCE=$SITE_ROOT"/deploy/nginx.conf"
NGINX_CONF_DEST="/etc/nginx/nginx.conf"

DB_NAME="lobbysearch"
DB_USER="lobbysearch"
DB_PASSWORD="lobbysearch"

VIRTUALENV_NAME="venv"

cd $SITE_ROOT
touch setup.log

echo "Updating packages."
sudo apt-get update >> setup.log

echo "Installing python3 and deps."
sudo apt-get install -y python3-dev python3-setuptools python3-pip libpq-dev build-essential >> setup.log

echo "Installing virtualenv."
sudo apt-get install -y virtualenv >> setup.log
sudo virtualenv $VIRTUALENV_NAME --python=python3 >> setup.log

echo "Installing nginx."
sudo apt-get install -y nginx >> setup.log
echo "Linking $SERVER_CONF_SOURCE to $SERVER_CONF_DEST"
sudo rm $SERVER_CONF_DEST
sudo ln -s $SERVER_CONF_SOURCE $SERVER_CONF_DEST >> setup.log

echo "Linking $NGINX_CONF_SOURCE to $NGINX_CONF_DEST."
echo "NOTE: this is ONLY required to fix a bug in vagrant / virtualbox, i.e. development ONLY."
sudo rm $NGINX_CONF_DEST
sudo ln -s $NGINX_CONF_SOURCE $NGINX_CONF_DEST >> setup.log

echo "Installing PostgreSQL."
sudo apt-get -y install postgresql >> setup.log

echo "Setting up database."
# switch to the postgres user
echo "create database $DB_NAME" | sudo -u postgres psql
echo "create role $DB_USER" | sudo -u postgres psql
echo "alter role $DB_USER with password '$DB_PASSWORD'" | sudo -u postgres psql
echo "alter role $DB_USER with login" | sudo -u postgres psql
echo "grant all privileges on database $DB_NAME to $DB_USER" | sudo -u postgres psql

echo "Installing redis server."
sudo apt-get -y install redis-server >> setup.log

echo "Installing required app packages."
source $VIRTUALENV_NAME"/bin/activate"
pip3 install -r requirements.txt >> setup.log

echo "Adding to .bashrc for easier ssh."
echo "cd $SITE_ROOT" >> /home/vagrant/.bashrc
echo "source $VIRTUALENV_NAME/bin/activate" >> /home/vagrant/.bashrc

echo "Server is set up."
