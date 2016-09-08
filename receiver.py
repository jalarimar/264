"""
Receiver Program.

"""
from sys import argv
import socket
import select
from common import *

CLOSE_REQUESTED = False

def receive(rin, rout, file):
    
    expected = 0
    
    while not CLOSE_REQUESTED:
        readable, _, _ = select.select([rin], [], [], 0.0005)
        if readable:
            sock = readable[0]
            message, address = rin.recvfrom(PACKET_SIZE)
            rcvd_pack = Packet.from_bytes(message)
            if rcvd_pack.magicno == 0x497E \
               and rcvd_pack.packet_type == Packet.DATA:
                ack_pack = Packet(bytes(), rcvd_pack.seqno,\
                 0x497E, Packet.ACK)
                rout.send(ack_pack.to_bytes())
                
                if rcvd_pack.seqno == expected:
                    expected = 1 - expected
                    if rcvd_pack.data_len > 0:
                        file.write(rcvd_pack.data)
                    else:
                        break
                        
                        
    print(expected)
    file.close()
    rin.close()
    rout.close()


def main(filename, ports):
    global CLOSE_REQUESTED
    CLOSE_REQUESTED = False
    
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
    return open(filename, 'wb')
    
    

if __name__ == '__main__':
    
    number_of_arguments = len(argv)
    if number_of_arguments != 5: # argv[0] is program name
        abort("Incorrect number of parameters")
        
    if number_of_arguments != len(set(argv)):
        abort("Port numbers not distinct")
        
    ports = tuple(int(p) for p in argv[1:4])
    for port in ports:
        if (port < 1024) or (port > 64000):
            abort("Port {} not within valid range \
            1024-64000".format(port)) 
    
    filename = argv[4]
    
    main(filename, ports)
