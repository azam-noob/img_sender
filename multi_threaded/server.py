import socket
import codecs
import struct
import threading
import os

ADDRESS = ("localhost", 12345)

# Create a socket to listen for client(s)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)
s.listen(2)

print("Waiting for connections...")

def receive_and_process_img(sc, file_name):
    # img_path = "data/{}.png".format(file_name)
    img_path = "{}.png".format(file_name)
    try:
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
        print("Saving image with name: ", img_path)
        f = open(img_path, "wb")
        f.write(codecs.decode(img_str, 'base64'))
        f.close()

        sc.send("Done!".encode())
    except Exception as e:
        print(e)
    finally:
        print("Closing socket")
        sc.close()


def accept_connection():
    i = 1
    while True:
        try:
            # Accept a connection
            sc, _ = s.accept()
            print("Accepted a connection!")
            rcv_sav_img = threading.Thread(target=receive_and_process_img, args=(sc, i))
            rcv_sav_img.start()
            i += 1
        except Exception as e:
            print(e)
    
    s.close()
            
 

accept = threading.Thread(target=accept_connection)
accept.start()

accept.join()
print("Exiting!!")
