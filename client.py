import base64
import struct
import socket
import sys

ADDRESS = ("localhost", 8877)

if len(sys.argv) < 2:
    print("Must pass the second argument as the path to the image.")
    exit(-1)

# Connect to server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDRESS)
print("Connected to the server!")

try:
    # Read the image string    
    print("Reading the image")
    img = open(sys.argv[1], "rb")
    img_str = base64.b64encode(img.read())
    print("Length of the image: ", len(img_str))

    # Send the size of the image first in four bytes.
    print("Sending the size of the image")
    len_str = struct.pack('!i', len(img_str))
    s.send(len_str)

    # img.close()

    # Send image as a string
    print("Sending the image")
    s.send(img_str)

    # Read response from the server
    print("Waiting for response")
    re = b''
    while len(re) == 0:
        re = s.recv(1024)

    print("Received: ", re.decode('ascii'))
except Exception as e:
    print(e)
finally:
    print("Closing socket...")
    s.close()

