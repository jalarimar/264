# this is how you use byte class to encode message:
# maxwell_has_stinky_socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# maxwell_has_stinky_socks.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

import sys
import socket

IP = '127.0.0.1'

def main():
    sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    if len(sys.argv[1:]) != 4: # argv[0] is program name
        print("Incorrect number of parameters")
        return
    if len(sys.argv[1:]) != len(set(sys.argv[1:])):
        print("Port numbers not distinct")
        return
    for channel_port in sys.argv[1:3]:
        if (channel_port < 1024) or (channel_port > 64000):
            print("Not within valid range")
            return
    
    sin.bind(IP, int(sys.argv[1]))
    sout.bind(IP, int(sys.argv[2]))
    
    csin_port = int(sys.argv[3]) # port to send to csin from sout
    sout.connect((IP, csin_port))    
    
    file_name_to_send = argv[4]
    # TODO: check whether that file exists, if not, exit
    send_file = open(file_name_to_send, 'r')
        
    nek = 0 # gonna be called next but python reserved word
    exitFlag = False
    
    while True:
        block = send_file.read(512)
        bytes_read = len(bytes(block, "utf8"))    
        if bytes_read == 0:
            packet = Packet(0x497E, "dataPacket", nek, 0, '')
            exitFlag = True
        elif bytes_read > 0:
            packet = Packet(0x497E, "dataPacket", nek, bytes_read, block)
        else:
            print("Negative bytes read?? Something went horrifically wrong")
            return
        packetBuffer = packet # place the packet into this buffer? wut how
    
        while exitFlag == False:
            # this is the inner loop of truth
            e = 9
    

main()