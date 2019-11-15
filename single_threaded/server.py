import socket
import codecs
import struct

ADDRESS = ("localhost", 8877)
IMG_NAME = "received_img.png"

# Create a socket to listen for client(s)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)
s.listen(2)

print("Waiting for connections...")

try:
    # Accept a connection
    sc, _ = s.accept()
    print("Accepted a connection!")

    # Receive image size in four bytes
    print("Receiving the size of the image")
    len_str = b''
    while len(len_str) == 0:
        len_str = sc.recv(4)
    size = struct.unpack('!i', len_str)[0]

    print("Size of the receiving image: ", size)

    img_str = b''

    # Receive the actall image
    print("Starting to receive the image")
    while size > 0:
        if size >= 4096:
            data = sc.recv(4096)
        else:
            data = sc.recv(size)

        if not data:
            break

        size -= len(data)
        img_str += data

    print("Size of the received image: ", len(img_str))

    # Save image on the hard
    print("Saving image with name: ", IMG_NAME)
    f = open(IMG_NAME, "wb")
    f.write(codecs.decode(img_str, 'base64'))
    f.close()

    sc.send("Got it!".encode())

except Exception as e:
    print(e)
finally:
    print("Closing socket...")
    s.close()
