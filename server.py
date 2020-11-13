import zmq
from flask import Flask

REV = "4"
ip = "192.168.178.20"
groupname = "test"

ctx = zmq.Context.instance()
socket = ctx.socket(zmq.RADIO)
socket.connect(f"udp://{ip}:5556")

i = 0
app = Flask(__name__)


@app.route("/")
def hello_world():
    global i
    # pub.send_string("%03i" % i)
    socket.send(b"%03i" % i, group=groupname)
    #    socket.send_multipart([groupname.encode("ascii"), b"%03i" % i])
    i += 1
    return f"rev {REV}, sent message to {ip}"
