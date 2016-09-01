"""
COSC264 2016 - Assignment

Written by:
  - Jessica Robertson
  - Maxwell Clarke (maxeonyx@gmail.com)

This is the module file for the common code in the sender, channel and reciever programs.

Currently, this can be run to spawn two threads, a receiver and a sender.
Run like the folowing:

    >>> python 264.py 4000 4001

where '4000' is the port to send to
and   '4001' is the port to receive from.

"""

import socket
import threading
from sys import argv

class Packet:
    '''This is the packet class. Vur exciting hur hur hur'''
    def __init__(self, magicno, packet_type, seqno, data_len, data):
        self.magicno = magicno # 0x497E, if different value then reject
        self.packet_type = packet_type # dataPacket or acknowledgementPacket
        self.seqno = seqno # restricted to 0 and 1
        self.data_len = data_len # between 0 and 512, num user bytes carried
        self.data = data # contains actual user data

def send():
    """
    Continually takes messages from input.
    Sends them via UDP to the port specified in the program arguments.
    """
    print("started send thread...")

    port = int(argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        s.sendto(input().encode('utf-8'), ("localhost", port))


def recv():
    """
    Continually recieves messages via UDP from the port specified in the program arguments.
    Prints the messages.
    """
    print("started recv thread...")

    port = int(argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("localhost", port))
    while True:
        message, address = s.recvfrom(1024)
        print("received: ", message)
    
def main():
    """
    Program begins here.
    """
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    sendThread = threading.Thread(target=send)
    sendThread.start()

if __name__ == "__main__":

    main()
