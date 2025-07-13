#  https://scapy.readthedocs.io/en/latest/
from scapy.all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
from scapy.layers.dns import DNS, DNSQR

googolIP = ""

def print_query_name(dns_packet):
    """This function prints the domain name from a DNS query"""
    print(dns_packet[DNSQR].qname, "--", dns_packet[DNS]["DNS Resource Record"].rdata)

def filter_dns(packet):
    """This function filters query DNS"""
    # [DNS].opcode= Query  and [DNSQR].qtype = 1 - is type A
    if (DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 1):
        # packet.show()
        global googolIP
        googolIP = packet[DNS]["DNS Resource Record"].rdata
        return True
    else:
        return False

print("Sending to google 'Hello'")
my_packet = IP(dst = "www.google.com")/ TCP(dport = 80) / Raw("Hello")
send(my_packet)

print("Starting to sniff!")
sniff(lfilter=filter_dns, prn=print_query_name, timeout=10)

# -----------------------------------------------------------------

def is_good(packet):
    return (TCP in packet and (packet[TCP].sport == 80 or packet[TCP].dport == 80))

def print_packet(packet):
    print(packet[IP].src, "-", packet[IP].dst)

def stopfilter(x):
    global googolIP
    if IP in x and x[IP].src == googolIP:  # src_ip
        return True
    else:
        return False

sniff(lfilter=is_good, prn=print_packet, stop_filter=stopfilter, timeout=10)
