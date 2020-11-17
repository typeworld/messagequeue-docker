import time
import zmq
import sys

ctx = zmq.Context.instance()
socket = ctx.socket(zmq.SUB)
# dish.rcvtimeo = 1000

groupname = "test"

socket.setsockopt(zmq.SUBSCRIBE, groupname.encode("ascii"))

# https://github.com/zeromq/libzmq/issues/2882
socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 10)
socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 1)
socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 1)


socket.connect(f"tcp://{sys.argv[-1]}:5556")
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
