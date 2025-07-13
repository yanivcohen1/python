import socket  # Import socket module
""" import traceback
except Exception as ex :
        print("error desc: ", ex)
        traceback.print_exc() """
# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = str(conn.recv(1024).decode())
                if not data:
                    break
                print("server recieved: " + data)
                conn.sendall(data.encode())
