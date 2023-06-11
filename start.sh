#!/usr/bin/env bash
python manage.py wait_for_db &&
python manage.py migrate &&
gunicorn --bind :8000 --workers 8 -t 60 bot_app.wsgi:application