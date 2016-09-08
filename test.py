from common import *
import sender.sender as sender
import channel.channel as channel
import receiver.receiver as receiver
import threading
import time
from hashlib import md5
from sys import argv

def start_channel():
    channel.main(0.1, (2000, 2001, 2002, 2003, 2004, 2005))
    
def start_receiver():
    receiver.main("testfile.out", (2005, 2007, 2003))

def start_sender():
    sender.main("testfile.in", (2002, 2006, 2000))
    
def main(num_tests=50):
    for _ in range(num_tests):
        receiver.CLOSE_REQUESTED = False
        sender.CLOSE_REQUESTED = False
        channel.CLOSE_REQUESTED = False
        
        chan_thread = threading.Thread(target=start_channel)
        recv_thread = threading.Thread(target=start_receiver)
        send_thread = threading.Thread(target=start_sender)

        chan_thread.start()
        time.sleep(1)
        recv_thread.start()
        time.sleep(1)
        send_thread.start()
        
        try:
            send_thread.join()
            recv_thread.join()
        except:
            print("TEST:     An exception occured: possibly")
            print("TEST:     the user interrupted the program")
            break
        finally:
            receiver.CLOSE_REQUESTED = True
            sender.CLOSE_REQUESTED = True
            channel.CLOSE_REQUESTED = True
            
            send_thread.join()
            recv_thread.join()
            chan_thread.join()
            in_sum = md5(open("testfile.in", "rb").read()).digest()
            out_sum = md5(open("testfile.out", "rb").read()).digest()
            print()
            print("TEST:     md5 sum {} match!".format("DOES" if in_sum == out_sum else "DOES NOT"))
        
if __name__ == "__main__":
    
    if len(argv) > 1:
        num_tests = int(argv[1])
        main(num_tests)
    else:
        main()