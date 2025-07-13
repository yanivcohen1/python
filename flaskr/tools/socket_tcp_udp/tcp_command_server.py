import random
import time
import socket

LISTEN_PORT = 5000
# Create a socket
listening_sock = socket.socket()

server_address = ('', LISTEN_PORT)
try:
    # Connecting to the port
    listening_sock.bind(server_address)

    # Starting to listen to the customer
    listening_sock.listen(1)

    while True:
        # Connecting to a conversation socket
        conv_sock, client_address = listening_sock.accept()

        # Receiving a message from the client
        message = conv_sock.recv(1024).decode()
        print(message)
        
        # Sending a message to the client according to the commands on the server
        if message.upper() == "NAME":
            conv_sock.send(("ADISERVER").encode())
        elif message.upper() == "RAND":
            conv_sock.send(str(random.randint(1, 10)).encode())
        elif message.upper() == "TIME":
            conv_sock.send((time.asctime()).encode())
        else:
            conv_sock.send(
                ("This is not a recognized server command").encode())
            # Closing the conversation socket
        conv_sock.close()
except OSError as ex:
    print("'exceptions' module: Error (%s)." % str(ex))
    print("The port is busy")
except KeyboardInterrupt : # control+C press
    listening_sock.shutdown(socket.SHUT_RDWR)
    listening_sock.close() 
