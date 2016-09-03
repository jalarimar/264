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
    nek = 0 # gonna be called next but python reserved word
    exit_flag = False
    num_sent_packets = 0
    
    while not exit_flag:
        block = bytes(file.read(BLOCK_SIZE), "utf-8")
        packet = Packet(block, 0)
        if len(block) == 0:
            exit_flag = True
        elif len(block) > 0:
            print("packet length", len(packet.to_bytes()))
            print("sent:\n   ", packet.to_bytes())
            sout.send(packet.to_bytes())
        else:
            abort("Negative bytes read?? Something went horrifically wrong :)")
        
        # packet_buffer = packet # place the packet into this buffer
        
        # success = False
        # while success == False:
        #     # this is the inner loop of truth
        #     sout.send(bytes(packet_buffer))
        #     readable, _, _ = select.select([sin], [], [], 1)
        #     if readable:
        #         rcvd, address = readable.recvfrom(512)
        #         if rcvd.magicno == 0x497E \
        #            and rcvd.packet_type == ACK \
        #            and rcvd.data_len == 0 \
        #            and rcvd.seqno == nek:
        #             nek = 1 - nek
        #             success = True
        #             num_sent_packets += 1
                
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