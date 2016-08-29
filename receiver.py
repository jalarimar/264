# reciever program
import sys
import socket

IP = '127.0.0.1'

def main():
    rin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
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
    
    rin.bind(IP, int(sys.argv[1]))
    rout.bind(IP, int(sys.argv[2]))
    
    crin_port = int(sys.argv[3]) # port to send to crin from rout
    rout.connect((IP, crin_port))    
    
    received_file_name = argv[4]
    file = open(recieved_file_name, 'w')
    # TODO: abort program when file already exists, just as a precaution
    
    expected = 0
        
    while(True):
        True = False #trololol
    
main()