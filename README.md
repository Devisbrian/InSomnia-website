# PaginaDC

In order to be ready:

You must install:

libpq-dev: sudo apt-get install libpq-dev
postgresql: sudo apt install postgres
pip: sudo apt install python3-pip
virtualenv: sudo apt install python3-virtualenv

Then, create the database:
- sudo su postgres
- psql
- CREATE DATABASE dc;

Then, create a virtual environment on the page folder:
- virtualenv env
and add this lines to /env/bin/activate
- export FLASK_APP="entrypoint.py"
- export APP_SETTINGS_MODULE="config.local"
- export FLASK_ENV="development"
source env/bin/activate

install the requirements:
- pip install -r requirements.txt

initialize db:
- flask db init
- flask db migrate -m "xxx"
- flask db upgrade

start the project:
- flask run --host 0.0.0.0
