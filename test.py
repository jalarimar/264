from common import *
import sender
import channel
import receiver
import threading
import time
from hashlib import md5
from sys import argv
from sys import stdout

def start_channel():
    channel.main(0.3, (2000, 2001, 2002, 2003, 2004, 2005))
    
def start_receiver():
    receiver.main("testfile.out", (2005, 2007, 2003))

def start_sender():
    sender.main("testfile.in", (2002, 2006, 2000))
    
def main(num_tests=1):
    for _ in range(num_tests):
        
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
            break
        finally:
            receiver.CLOSE_REQUESTED = True
            sender.CLOSE_REQUESTED = True
            channel.CLOSE_REQUESTED = True
            
            send_thread.join()
            recv_thread.join()
            chan_thread.join()
            in_sum = md5(
                open("testfile.in", "rb").read())
                .digest()
            out_sum = md5(
                open("testfile.out", "rb").read())
                .digest()
            
            stdout.flush()
        
if __name__ == "__main__":
    
    if len(argv) > 1:
        num_tests = int(argv[1])
        main(num_tests)
    else:
        main()