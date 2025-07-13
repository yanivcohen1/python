#!/usr/bin/python           # This is server.py file
import socket  # Import socket module
import json
import traceback
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # for tcp
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # for udp

host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
sock.bind((host, port))  # Bind to the port

# A forever loop until we interrupt it or
# an error occurs
while True:
    try:
        # Receive data from the client
        data, addr = sock.recvfrom(1024)
        # print recv msg
        msg = str(data.decode())
        print("server recv:", msg)
        msg_dict: dict = json.loads(msg)
        # print("json keys:", msg_dict.keys())
        for key in msg_dict:
            print(key,":", msg_dict[key])
        # for udp echo
        sock.sendto(msg.encode(), addr)
    except Exception as ex :
        print("error desc: ", ex)
        traceback.print_exc()
