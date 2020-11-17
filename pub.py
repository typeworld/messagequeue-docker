import os
import json
import zmq

# ZMQ
ctx = zmq.Context.instance()
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://0.0.0.0:5556")


def send(topic, message):
    topic = str(topic)
    message = str(message)
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


@app.route("/publish", methods=["POST"])
def publish():

    # Authorization
    if not g.form.get("apiKey") == os.getenv("APIKEY"):
        return abort(401)

    # Send message
    payload = {"command": "update", "lastUpdated": g.form.get("lastUpdated")}
    send(g.form.get("topic"), json.dumps(payload))

    return "ok"
