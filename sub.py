import time
import zmq
import sys

ctx = zmq.Context.instance()
socket = ctx.socket(zmq.SUB)
# dish.rcvtimeo = 1000

groupname = "test"

socket.connect(f"tcp://{sys.argv[-1]}:5556")
socket.setsockopt(zmq.SUBSCRIBE, groupname.encode("ascii"))
# socket.subscribe("light")

while True:
    time.sleep(0.1)
    try:
        topic, msg = socket.recv_multipart()
        # msg = socket.recv_string()
    except zmq.Again:
        print(".")
        continue
    print("Received %s:%s" % (topic, msg))
    # print("Received %s" % (msg))

dish.close()
ctx.term()
