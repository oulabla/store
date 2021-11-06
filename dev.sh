#!/usr/bin/env bash
# echo 'Start venv'
# source venv/bin/activate
echo 'Start Postgres'
sudo /etc/init.d/postgresql restart
# echo 'Start Dev Server'
# adev runserver app/main.py
#export PYTHONPATH="./" && python store/app.py

# alembic revision --autogenerate -m "add root_cause table"