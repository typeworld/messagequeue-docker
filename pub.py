import os
import json
import zmq
import logging

# ZMQ
ctx = zmq.Context.instance()
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://0.0.0.0:5556")


def send(topic, message):
    topic = str(topic)
    message = str(message)
    logging.warning(f"sending {topic}: {message}")
    socket.send_multipart([topic.encode("ascii"), message.encode("ascii")])


# Flask app
from flask import Flask, abort, g, request

app = Flask(__name__)

# Prepare form data
class Form(dict):
    def get(self, key):
        if key in self:
            return self[key]
        else:
            return None


# Prepare form data
@app.before_request
def before_request_webapp():
    g.form = Form()
    for key in request.values:
        g.form[key] = request.values.get(key)


@app.route("/uptime", methods=["GET"])
def uptime():
    return "ok"


@app.route("/publish", methods=["POST"])
def publish():

    # Authorization
    if os.getenv("APIKEY") and g.form.get("apiKey"):
        APIKEY = os.getenv("APIKEY").strip()
        FORMAPIKEY = g.form.get("apiKey").strip()
        if FORMAPIKEY != APIKEY:
            return abort(401)
    else:
        return abort(401)

    if not g.form.get("topic"):
        return "topic parameter missing"

    if not g.form.get("command"):
        return "command parameter missing"

    # Send message
    payload = {
        "command": g.form.get("command"),
    }
    # Optional
    if g.form.get("serverTimestamp"):
        payload["serverTimestamp"] = g.form.get("serverTimestamp")
    if g.form.get("sourceAnonymousAppID"):
        payload["sourceAnonymousAppID"] = g.form.get("sourceAnonymousAppID")
    if g.form.get("delay"):
        payload["delay"] = g.form.get("delay")

    send(g.form.get("topic"), json.dumps(payload))

    return "ok"
