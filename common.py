"""
COSC264 2016 - Assignment

Written by:
  - Jessica Robertson
  - Maxwell Clarke (maxeonyx@gmail.com)

This is the module file for the common code in the sender, channel and reciever programs.

Currently, this can be run to spawn two threads, a receiver and a sender.
Run like the folowing:

    >>> python common.py 4000 4001

where '4000' is the port to send to
and   '4001' is the port to receive from.

"""
import struct
import socket
import threading
from sys import argv


HOST_IP = "127.0.0.1"
BLOCK_SIZE = 512
# Packet size has four ints in addition to the data
PACKET_SIZE = BLOCK_SIZE + 4*4


class Packet:
    """
    Class to encapsulate a packet.
    TODO: Serialize to a utf-8 string and back
    """
    STRUCT_FORMAT = struct.Struct("iiii{BLOCK_SIZE}s".format(BLOCK_SIZE=BLOCK_SIZE))
    
    ACK = 1
    DATA = 2
    
    def __init__(self, data, seqno, magicno=0x497E, packet_type=DATA):
        self.magicno = magicno # 0x497E, if different value then reject
        self.packet_type = packet_type # dataPacket or acknowledgementPacket
        self.seqno = seqno # restricted to 0 and 1
        self.data = data
        
        if len(data) <= BLOCK_SIZE:
            self.data_len = len(data)
        else:
            abort("Data too long. Must be {BLOCK_SIZE} bytes or less".format(BLOCK_SIZE=BLOCK_SIZE))
            
        
    def to_bytes(self):
        return Packet.STRUCT_FORMAT.pack(
            self.magicno,
            self.packet_type,
            self.seqno,
            self.data_len,
            self.data
        )
        
    @classmethod
    def from_bytes(cls, bytestring):
        magicno, packet_type, seqno, data_len, data = Packet.STRUCT_FORMAT.unpack(bytestring)
        return Packet(data, seqno, magicno, packet_type)
        
    def get_data(self):
        return self.data.decode("utf-8")


def abort(message):
    """
    Aborts the program with a message
    """
    print(message)
    exit()
    
    
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
