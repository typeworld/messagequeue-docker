import zmq
from flask import Flask

REV = "4"

ctx = zmq.Context.instance()
radio = ctx.socket(zmq.RADIO)

ip = "35.196.237.158"
groupname = "test"
radio.connect(f"udp://{ip}:5556")

i = 0
app = Flask(__name__)


@app.route("/")
def hello_world():
    radio.send(b"%03i" % i, group=groupname)
    return f"rev {REV}, sent message to {ip}"
