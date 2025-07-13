#  DNS להדפיס את כל הדומיינים שעבורם מתבצעת שאילתת
from scapy.all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
from scapy.layers.l2 import ARP


def findAllComputersInLocalNet():
    computers = []
    ips = "192.168.0.0/24"
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ips)
    answer, unanswered = srp(ether / arp, timeout=2, inter=0.1)
    for sent, received in answer:
        print(received.summary())
        # received.show()
        if received.haslayer(ARP):
            ip_dict = {}
            ip_dict["mac"] = received[ARP].hwsrc
            ip_dict["ip"] = received[ARP].psrc
        computers.append(ip_dict)
    # for computer in computers:
    # print(computer)
    return computers


# cap = sniff(count=15)
def is_good(packet):
    if packet.haslayer(ARP):
        # packet.show()
        print("mac:", packet[ARP].hwsrc, "- ip:", packet[ARP].psrc)
        return True
    else:
        return False


computers_ip_mac = findAllComputersInLocalNet()

# print the mac number
cap = sniff(lfilter=is_good, timeout=15)
