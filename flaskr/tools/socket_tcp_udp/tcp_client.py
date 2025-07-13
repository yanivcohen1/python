import socket               # Import socket module
import traceback

# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        msg = input("enter msg:")
        if "end" == msg:
            break
        sock.sendall(msg.encode())
        data = str(sock.recv(1024).decode())
        print("client received: " + data)
