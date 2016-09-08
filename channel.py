from sys import argv
import socket
from select import select
import random
from common import *

CLOSE_REQUESTED = False

def channel(packet_loss_rate, csin, csout, crin, crout):
    global CLOSE_REQUESTED
    while not CLOSE_REQUESTED:
        readable_sockets, _, _ = select([csin, crin], [], [], 0.0002)
        for sock in readable_sockets:
            rcvd, address = sock.recvfrom(PACKET_SIZE)
            packet = Packet.from_bytes(rcvd)
            
            if packet.magicno != 0x497E or \
            random.random() <= packet_loss_rate:
                continue
                
            try:
                if sock == csin:
                    crout.send(packet.to_bytes())
                elif sock == crin:
                    csout.send(packet.to_bytes())
            except:
                CLOSE_REQUESTED = True
                break
    
    csin.close()
    csout.close()
    crin.close()
    crout.close()

def main(packet_loss_rate, ports):
    global CLOSE_REQUESTED
    CLOSE_REQUESTED = False
        
    channel(packet_loss_rate, *setup_sockets(*ports))
    
    
            
def setup_sockets(c_s_in_port, c_s_out_port,\
     s_in_port, c_r_in_port,\
     c_r_out_port, r_in_port):
            
    csin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    crin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    crout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    csin.bind((HOST_IP, c_s_in_port))
    csout.bind((HOST_IP, c_s_out_port))  
    crin.bind((HOST_IP, c_r_in_port))
    crout.bind((HOST_IP, c_r_out_port))
    
    csout.connect((HOST_IP, s_in_port))
    crout.connect((HOST_IP, r_in_port))
    
    return csin, csout, crin, crout
                    
if __name__ == "__main__":
    
    number_of_arguments = len(argv)
    if number_of_arguments != 8: # argv[0] is program name
        abort("Incorrect number of parameters")
        
    if number_of_arguments != len(set(argv)):
        abort("Port numbers not distinct")
    
    ports = tuple(int(p) for p in argv[1:7])
    for port in ports:
        if (port < 1024) or (port > 64000):
            abort("Port {} not within valid range \
            1024-64000".format(port))
    
    packet_loss_rate = float(argv[7])
    if (packet_loss_rate < 0) or (packet_loss_rate >= 1):
        abort("Incorrect packet loss rate, must be \
        between 0 and 1")
        
    main(packet_loss_rate, ports)
