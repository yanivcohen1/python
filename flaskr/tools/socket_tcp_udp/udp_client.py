#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
import json
import  traceback

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

server = (host, port)
while True:
    try:
        # msg = input("Enter the msg:")
        msg = {"user": "yaniv", "port": 5}
        msg_txt = json.dumps(msg)
        msg_in = input("insert format: " + msg_txt)
        sock.sendto(msg_in.encode(), server)
        data, addr = sock.recvfrom(1024)
        msg = str(data.decode())
        print("client recv:", msg)
        msg_dict: dict = json.loads(msg)
        for key in msg_dict:
            print(key,":", msg_dict[key])
    except Exception as ex :
        print("error desc: ", ex)
        traceback.print_exc()

sock.close()