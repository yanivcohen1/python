import socket

LISTEN_PORT = 2000
# Create a socket
listening_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('', LISTEN_PORT)
# Connecting to the port
listening_sock.bind(server_address)

while True:
    # Receiving a message from the client
    try:
        (client_data, client_address) = listening_sock.recvfrom(1024)
        print("server rcv: ", client_data) 
        # Sending a message to the client according to the commands on the server
        listening_sock.sendto("the server sent: ".encode() + client_data, client_address)
        print("server-send: ", client_data)
        # listening_sock.close()
    except Exception as ex:
        print("server error: ", ex)   
