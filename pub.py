from flask import Flask
import random

import zmq
import zmq.utils.monitor

# Metrics
subscribers = 0

# # Environment
# GCE = os.getenv("HOSTNAME") == "messagequeue"

groupname = "test"

# ZMQ
ctx = zmq.Context.instance()
socket = ctx.socket(zmq.PUB)
# https://github.com/zeromq/libzmq/issues/2882

# socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
# # the number of unacknowledged probes to send before considering the
# # connection dead and notifying the application layer
# socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 10)
# # the interval between the last data packet sent
# # (simple ACKs are not considered data) and the first keepalive probe;
# # after the connection is marked to need keepalive, this counter is
# # not used any further
# socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 10)
# # the interval between subsequential keepalive probes, regardless of
# # what the connection has exchanged in the meantime
# socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 10)

# # ZMQ Monitoring
# EVENT_MAP = {}
# print("Event names:")
# for name in dir(zmq):
#     if name.startswith("EVENT_"):
#         value = getattr(zmq, name)
#         print("%21s : %4i" % (name, value))
#         EVENT_MAP[value] = name


# def event_monitor(monitor):
#     while monitor.poll():
#         evt = recv_monitor_message(monitor)
#         evt.update({"description": EVENT_MAP[evt["event"]]})
#         if not GCE:
#             logging.warning("Event: {}".format(evt))
#         if evt["event"] == zmq.EVENT_MONITOR_STOPPED:
#             break

#         # Subscriber tracking
#         global subscribers
#         if evt["event"] == zmq.EVENT_HANDSHAKE_SUCCEEDED:
#             subscribers += 1
#             updateMonitoring()
#         if evt["event"] == zmq.EVENT_DISCONNECTED:
#             subscribers -= 1
#             if subscribers < 0:
#                 subscribers = 0
#             updateMonitoring()

#     monitor.close()
#     logging.warning("event monitor thread done!")


# # Start ZMQ + monitoring
# monitor = socket.get_monitor_socket()
# monitorThread = threading.Thread(target=event_monitor, args=(monitor,))
# monitorThread.start()

socket.bind("tcp://0.0.0.0:5556")

i = 0
app = Flask(__name__)


def send(topic, message):
    topic = str(topic)
    message = str(message)
    socket.send_multipart([topic.encode("ascii"), message.encode("ascii")])


@app.route("/")
def hello_world():

    global i
    send(groupname, i)
    i += 1

    return "sent message"


@app.route("/random/<max>")
def sendrandom(max):

    i = random.randint(0, int(max))
    send(f"{i}a", i)

    return f"sent message to {i}"
