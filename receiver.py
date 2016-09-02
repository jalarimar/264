"""
Receiver Program.

"""
from sys import argv
import socket
from common import *


def receive(rin, rout, file):
    
    while True:
        message, address = rin.recvfrom(PACKET_SIZE)
        packet = Packet.from_bytes(message)
        file.write(packet.get_data())
        print(packet.get_data(), end='')


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
    
    rin, rout = setup_sockets(ports[0], ports[1], ports[2])
    
    receive(rin, rout, file)
    
        
def setup_sockets(r_in_port, r_out_port, c_r_in_port):
    """
    Create and bind the reciever_in and receiver_out sockets.
    """
    rin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    rin.bind((HOST_IP, r_in_port))
    rout.bind((HOST_IP, r_out_port))
    
    rout.connect((HOST_IP, c_r_in_port))
    
    return rin, rout
    
    
    
def setup_file(filename):
    """
    Opens the output file for write
    """
    return open(filename, 'w')
    # TODO: do we want to abort if the file already exists
    
    

    
    
main()