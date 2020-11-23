#!/bin/sh

# Monitoring
python /app/monitoring.py &

# Server
gunicorn --config gunicorn_config.py pub:app
