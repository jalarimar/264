# hash tag awesome
import sys
import socket
import random

IP = '127.0.0.1'


def main():
    # look I used returns m7
    csin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    crin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    crout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    
    if len(sys.argv[1:]) != 7: # argv[0] is program name
        print("Incorrect number of parameters")
        return
    if len(sys.argv[1:]) != len(set(sys.argv[1:])):
        print("Port numbers not distinct")
        return
    for channel_port in sys.argv[1:5]:
        if (channel_port < 1024) or (channel_port > 64000):
            print("Not within valid range")
            return
    
    csin.bind(IP, int(sys.argv[1]))
    csout.bind(IP, int(sys.argv[2]))  
    crin.bind(IP, int(sys.argv[3]))
    crout.bind(IP, int(sys.argv[4]))
    
    sin_port = int(sys.argv[5]) # port to send to sin from csout
    csout.connect((IP, sin_port))
    rin_port = int(sys.argv[6]) # port to send to rin from crout
    crout.connect((IP, rin_port))
    
    packet_loss_rate = float(sys.argv[7])
    if (packet_loss_rate < 0) or (packet_loss_rate >= 1):
        print("Incorrect packet loss rate")
        return
    
    while(True):
        s_readable, s_writable, s_exceptional = select.select([csin], [], [], 1)
        r_readable, r_writable, r_exceptional = select.select([crin], [], [], 1)
        if s_readable:
            rcvd, address = s_readable.recvfrom(512)
            if rcvd.magicno == 0x497E:
                if random.random() >= packet_loss_rate:
                    crout.send(bytes(rcvd))
        elif r_readable:
            rcvd, address = r_readable.recvfrom(512)
            if rcvd.magicno == 0x497E:
                if random.random() >= packet_loss_rate:
                    csout.send(bytes(rcvd))        
                    

main()