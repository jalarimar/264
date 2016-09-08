# this is how you use byte class to encode message:
# maxwell_has_stinky_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# maxwell_has_stinky_socks.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

from sys import argv
import socket
import select
from common import *

CLOSE_REQUESTED = False

def send(sin, sout, file):
    """
    Send thread. Sends the file contents to a receiver via the channel.
    
    """
    _next = 0
    exit_flag = False
    num_sent_packets = 0
    
    while not (exit_flag or CLOSE_REQUESTED):
        #print("SENDER:   reading {} bytes".format(BLOCK_SIZE))
        block = file.read(BLOCK_SIZE)
        if len(block) == 0:
            exit_flag = True
            packet = Packet(bytes(), _next)
        else:
            packet = Packet(block, _next)
            
        while not CLOSE_REQUESTED:
            #print("SENDER:   try send {} bytes".format(PACKET_SIZE))
            try:
                sout.send(packet.to_bytes())
                num_sent_packets += 1
                print("sent ", num_sent_packets)
            except:
                print("locked")
                break
            readable, _, _ = select.select([sin], [], [], 1)
            if readable:
                sock = readable[0]
                packet_bytes, address = sock.recvfrom(PACKET_SIZE)
                packet = Packet.from_bytes(packet_bytes)
                if packet.magicno == 0x497E \
                   and packet.packet_type == Packet.ACK \
                   and packet.data_len == 0 \
                   and packet.seqno == _next:
                    _next = 1 - _next
                    break
    
    #print()
    #print("SENDER:   sent {} packets!".format(num_sent_packets))
    print(num_sent_packets)
    #print()
    #print("SENDER:   CLOSING") 
    print(_next)
    file.close()
    sin.close()
    sout.close()
    

def main(filename, ports):
    global CLOSE_REQUESTED
    CLOSE_REQUESTED = False
    
    file = setup_file(filename)
    
    sin, sout = setup_sockets(ports[0], ports[1], ports[2])
    
    send(sin, sout, file)
            
            
def setup_sockets(s_in_port, s_out_port, c_s_in_port):
    """
    Create and bind the sender_in and sender_out sockets.
    """
    sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sin.bind((HOST_IP, s_in_port))
    sout.bind((HOST_IP, s_out_port))
    
    sout.connect((HOST_IP, c_s_in_port))   
    
    return sin, sout 
    
    
def setup_file(filename):
    """
    Opens the input file for read
    """
    return open(filename, 'rb')
        

if __name__ == '__main__':
    
    number_of_arguments = len(argv)
    if number_of_arguments != 5: # argv[0] is program name
        abort("Incorrect number of parameters")
        
    if number_of_arguments != len(set(argv)):
        abort("Port numbers not distinct")
    
    ports = tuple(int(p) for p in argv[1:4])
    for port in ports:
        if (port < 1024) or (port > 64000):
            abort("Port {} not within valid range 1024-64000".format(port))
    
    filename = argv[4]
    
    main(filename, ports)
