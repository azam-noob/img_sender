import base64
import struct
import socket
import sys
import threading
import os
from shutil import copyfile

ADDRESS = ("localhost", 12345)

if len(sys.argv) < 3:
    print("Must pass the second argument as the path to the image and third argument as the number of clinets.")
    exit(-1)

CLIENTS = int(sys.argv[2])

for i in range(CLIENTS):
    name = "{}.png".format(i)
    print("Creating ", name)
    copyfile(sys.argv[1], name)

def send_to_server (client_id):
    print("Starting client ", client_id)

    # Connect to server.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)
    print("Connected to the server for client ", client_id)
    
    try:
        # Read the image string    
        print("Reading the image client ", client_id)
        img = open("{}.png".format(client_id), "rb")
        img_str = base64.b64encode(img.read())
        print("Length of the image: ", len(img_str), " client ",  client_id)
    
        # Send the size of the image first in four bytes.
        print("Sending the size of the image client", client_id)
        len_str = struct.pack('!i', len(img_str))
        s.send(len_str)
    
        img.close()
    
        # Send image as a string
        print("Sending the image client ", client_id)
        s.send(img_str)
    
        # Read response from the server
        print("Waiting for response for client ", client_id)
        re = b''
        while len(re) == 0:
            re = s.recv(1024)
    
        print("Received: ", re.decode('ascii'), " client ", client_id)
    except Exception as e:
        print(e)
    finally:
        print("Closing socket for client ", client_id)
        s.close()

threads = []
for i in range(CLIENTS):
    threads.append(threading.Thread(target = send_to_server, args = (i, )))
    threads[i].start()

for i in range(CLIENTS):
    threads[i].join()


for i in range(CLIENTS):
    name = "{}.png".format(i)
    print("Removing: ", name)
    os.remove(name)
