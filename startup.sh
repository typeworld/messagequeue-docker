#!/bin/sh
# python -u /app/server.py
# gunicorn --config gunicorn_config.py app.wsgi:app

gunicorn --config gunicorn_config.py pub:app

# 18:35:53.476958 IP instance-1.us-central1-a.c.typeworld2.internal.47648 > 252.143.223.35.bc.googleusercontent.com.freeciv: UDP, length 8
# 18:35:53.478529 IP 252.143.223.35.bc.googleusercontent.com.47648 > instance-1.us-central1-a.c.typeworld2.internal.freeciv: UDP, length 8

# 18:37:18.817899 IP 172.17.0.2.34143 > ping: UDP, length 8
# 18:37:18.819284 IP 252.143.223.35.bc.googleusercontent.com.34143 > 172.17.0.2.freeciv: UDP, length 8

