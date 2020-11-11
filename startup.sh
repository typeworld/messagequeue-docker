#!/bin/sh
# python -u /app/server.py
# gunicorn --config gunicorn_config.py app.wsgi:app

gunicorn --config gunicorn_config.py server:app
