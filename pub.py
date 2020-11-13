import zmq
from flask import Flask

REV = "4"
ip = "0.0.0.0"
groupname = "test"

ctx = zmq.Context.instance()
socket = ctx.socket(zmq.PUB)
socket.bind(f"tcp://{ip}:5556")

i = 0
app = Flask(__name__)


@app.route("/")
def hello_world():
    global i
    # pub.send_string("%03i" % i)
    # socket.send(b"%03i" % i, group=groupname)
    socket.send_multipart([groupname.encode("ascii"), b"%03i" % i])
    # socket.send_string("%03i" % i)
    # socket.send_string("light is ON")
    i += 1
    return f"rev {REV}, sent message to {ip}"
