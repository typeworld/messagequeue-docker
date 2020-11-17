import time
import zmq
import threading
import sys

latestNumber = None
received = 0
subscribers = 0
firstReceived = 0

numberOfSubscribers = 1000


def recv(i):

    global latestNumber, received, firstReceived

    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)

    socket.setsockopt(zmq.SUBSCRIBE, f"{i}a".encode("ascii"))

    # https://github.com/zeromq/libzmq/issues/2882

    socket.setsockopt(zmq.TCP_KEEPALIVE, 1)

    # following explanations are from https://tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/#whatis
    # the number of unacknowledged probes to send before considering the
    # connection dead and notifying the application layer
    socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 10)
    # the interval between the last data packet sent
    # (simple ACKs are not considered data) and the first keepalive probe;
    # after the connection is marked to need keepalive, this counter is
    # not used any further
    socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 30)
    # the interval between subsequential keepalive probes, regardless of
    # what the connection has exchanged in the meantime
    socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 30)

    socket.connect("tcp://34.73.146.178:5556")

    while True:
        time.sleep(0.1)
        topic, msg = socket.recv_multipart()
        print(f"Received {i}, {topic.decode()}")


def observe():
    global latestNumber, received, firstReceived
    while True:

        print(received * 100 / numberOfSubscribers, "%")
        time.sleep(1)


start = int(sys.argv[-1])
for i in range(start, start + numberOfSubscribers):
    t = threading.Thread(target=recv, args=(i,))
    t.start()
    subscribers += 1

# t = threading.Thread(target=observe)
# t.start()

print(f"Created {subscribers} subscribers")
