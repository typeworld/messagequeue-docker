import time
import zmq
import threading
import sys

groupname = "test"
latestNumber = None
received = 0
subscribers = 0
firstReceived = 0

numberOfSubscribers = 1024


def recv():

    global latestNumber, received, firstReceived

    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)

    socket.setsockopt(zmq.SUBSCRIBE, groupname.encode("ascii"))

    # https://github.com/zeromq/libzmq/issues/2882
    socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
    socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 10)
    socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 1)
    socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 1)

    socket.connect("tcp://34.73.146.178:5556")

    while True:
        time.sleep(0.1)
        topic, msg = socket.recv_multipart()
        number = msg.decode()
        if latestNumber != number:
            firstReceived = time.time()
            received = 1
            latestNumber = number
            print("Reset")
        else:
            received += 1


def observe():
    global latestNumber, received, firstReceived
    while True:

        print(received * 100 / numberOfSubscribers, "%")
        time.sleep(1)


for i in range(numberOfSubscribers):
    t = threading.Thread(target=recv)
    t.start()
    subscribers += 1

t = threading.Thread(target=observe)
t.start()

print(f"Created {subscribers} subscribers")
