import time
import zmq

ctx = zmq.Context.instance()
radio = ctx.socket(zmq.RADIO)

groupname = "test"
radio.connect("udp://35.227.7.198:5556")


def do_main_program():
    i = 0
    while True:
        print("Sending %03i" % i)
        radio.send(b"%03i" % i, group=groupname)
        time.sleep(3)
        i += 1


if __name__ == "__main__":
    do_main_program()
