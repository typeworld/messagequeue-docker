import time
import zmq
import sys

ctx = zmq.Context.instance()
socket = ctx.socket(zmq.SUB)
# dish.rcvtimeo = 1000

groupname = "test"

socket.setsockopt(zmq.SUBSCRIBE, "test1".encode("ascii"))
socket.setsockopt(zmq.SUBSCRIBE, "test2".encode("ascii"))

# https://github.com/zeromq/libzmq/issues/2882
socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 10)
socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 30)
socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 30)


socket.connect(f"tcp://{sys.argv[-1]}:5556")
# socket.subscribe("light")

while True:
    time.sleep(0.1)
    topic, msg = socket.recv_multipart()
    print("Received %s:%s" % (topic.decode(), msg.decode()))

dish.close()
ctx.term()
