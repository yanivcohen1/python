import json
from collections import defaultdict
from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.inet import UDP, TCP, IP, Ether
from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse

# Dictionary to store requests by the transaction ID
requests = defaultdict(dict)
# Define the IP address and port to filter
target_ip = "54.187.16.171"
target_port = 80

def process_packet(packet):
    if packet.haslayer(HTTPRequest) and packet[IP].dst == target_ip:
        # Modify the HTTP request
        print("req:",packet)
        if packet.haslayer(Raw) and b'application/json' in packet[HTTPRequest].Content_Type:
            print("payload:", packet[Raw].load)
        # Extract request information
        http_request = packet[HTTPRequest]
        transaction_id = (packet[IP].src, packet[TCP].dport, packet[TCP].seq)
        url = f"http://{http_request.Host.decode()}{http_request.Path.decode()}"

        # Store URL with the transaction ID
        requests[transaction_id]['url'] = url
        if packet[HTTPRequest].Path == b"/user/" and packet.haslayer(Raw):
            payload_bin = packet[Raw].load
            payload_dict = json.loads(payload_bin)
            if packet[HTTPRequest].Method == b"POST":
                print(f"user:{payload_dict[0]}")
                print(f"password:{payload_dict[1]}")
            if packet[HTTPRequest].Method == b"PUT":
                print(f'user:{payload_dict["user_name"]}')
                print(f'password:{payload_dict["password"]}')
        # Send the modified packet back
        # packet[HTTPRequest].Method = "GET"
        # packet[HTTPRequest].Path = "/new-path"
        # sendp(packet) # , iface="eth0"

    if packet.haslayer(HTTPResponse) and packet[IP].src == target_ip:
        transaction_id = (packet[IP].dst, packet[TCP].sport, packet[TCP].ack - 1)
        if transaction_id in requests:
            # Retrieve and print the URL
            url = requests[transaction_id].get('url')
            if url:
                print(f"res_URL: {url}")
        if packet.haslayer(Raw) and b'application/json' in packet[HTTPResponse].Content_Type:
            if packet[Raw].load != b'[]':
                print("res:",packet)
                print("res:",packet[Raw].load)

# Sniff HTTP packets from the specified IP and port
sniff(filter=f"tcp and host {target_ip} and port {target_port}", prn=process_packet, store=False)
