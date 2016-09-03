# this is how you use byte class to encode message:
# maxwell_has_stinky_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# maxwell_has_stinky_socks.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

from sys import argv
import socket
import select
from common import *

def send(sin, sout, file):
    """
    Send thread. Sends the file contents to a receiver via the channel.
    
    """
    _next = 0
    exit_flag = False
    num_sent_packets = 0
    
    while not exit_flag:
        print("reading {} bytes".format(BLOCK_SIZE))
        block = bytes(file.read(BLOCK_SIZE), "utf-8")
        if len(block) == 0:
            exit_flag = True
            packet = Packet(bytes(), _next)
        else:
            packet = Packet(block, _next)
            
        while True:
            print("attemping to send a {} byte packet".format(PACKET_SIZE))
            sout.send(packet.to_bytes())
            readable, _, _ = select.select([sin], [], [], 1)
            if readable:
                sock = readable[0]
                packet_bytes, address = sock.recvfrom(PACKET_SIZE)
                packet = Packet.from_bytes(packet_bytes)
                if packet.magicno == 0x497E \
                   and packet.packet_type == ACK \
                   and packet.data_len == 0 \
                   and packet.seqno == _next:
                   _next = 1 - _next
                   num_sent_packets += 1
                   break

    file.close()
    sin.close()
    sout.close()
    print(num_sent_packets)
    
    

def main():
    
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
    return open(filename, 'r')
        

                
    

main()