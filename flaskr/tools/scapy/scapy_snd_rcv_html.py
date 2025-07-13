from scapy.all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
# ip.src == 104.70.125.117 or ip.dst == 104.70.125.117
SERVER = ""
def stopfilter(packet):
    if IP in packet and packet[IP].src == SERVER and packet.haslayer(Raw):  # src_ip
        # print(packet.getlayer(Raw).load.decode())
        return True
    else:
        return False

def get_html(url, path):
    # create a TCP SYN packet
    syn_packet = IP(dst=url)/TCP(dport=80, flags="S")
    # send the SYN packet and receive the SYN-ACK packet
    syn_ack_packet = sr1(syn_packet)
    # create an ACK packet
    ack_packet = IP(dst=url)/TCP(dport=80, flags='A', seq=syn_ack_packet[TCP].ack,
                                ack=syn_ack_packet[TCP].seq + 1)
    # send the ACK packet and receive the HTTP response
    http_response = sr1(ack_packet/Raw(load="GET /{0} HTTP/1.1\r\nHost: {1}\r\n\r\n".format(path, url)))
    global SERVER
    SERVER = http_response[IP].src
    # http_response.show()
    cap = sniff(filter="tcp port " + str(80), stop_filter=stopfilter)
    for packet in cap:
      if packet.haslayer(Raw):
        return packet[Raw].load.decode()
    return None

html = []
html.append(get_html("ynet.co.il", "news/category/184"))
html.append(get_html("google.com", ""))
for html1 in html:
    print(html1)
