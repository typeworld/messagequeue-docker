import time
import zmq
import sys

ctx = zmq.Context.instance()
dish = ctx.socket(zmq.DISH)
dish.rcvtimeo = 1000

groupname = "test"

dish.bind(f"udp://{sys.argv[-1]}:5556")
dish.join(groupname)

while True:
    time.sleep(0.1)
    try:
        msg = dish.recv(copy=False)
    except zmq.Again:
        print(".")
        continue
    print("Received %s:%s" % (msg.group, msg.bytes.decode("utf8")))

dish.close()
ctx.term()
