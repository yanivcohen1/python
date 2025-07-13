#  DNS להדפיס את כל הדומיינים שעבורם מתבצעת שאילתת
from scapy.all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
from scapy.layers.dns import DNS, DNSQR

def getIP(domain):
    SERVER_IP = "8.8.8.8"
    DPORT = 53
    fullmsg = IP(dst=SERVER_IP)/UDP(dport=DPORT)/DNS(rd=1,qd=DNSQR(qname=domain))
    ans = sr1(fullmsg, verbose=0)
    # print(ans.show())
    print(domain + " -", ans["DNS"]["DNS Resource Record"].rdata)

getIP("ynet.co.il")
# ---------------BY SMIFF--------------------------------------------------

def send_dns(domain):
  #domain = "ynet.co.il"
  SERVER_IP = "8.8.8.8"
  DPORT = 53
  fullmsg = IP(dst=SERVER_IP)/UDP(dport=DPORT)/DNS(rd=1,qd=DNSQR(qname=domain))
  send(fullmsg)

def print_query_name(dns_packet):
    """This function prints the domain name from a DNS query"""
    print(dns_packet[DNSQR].qname, "--", dns_packet[DNS]["DNS Resource Record"].rdata)

def filter_dns(packet):
    """This function filters query DNS"""
    # [DNSQR].qtype: https://elementor.com/resources/glossary/what-are-dns-record-types/?utm_source=google&utm_medium=cpc&utm_campaign=13060922353&utm_term=&gclid=CjwKCAjwsvujBhAXEiwA_UXnABmjX08JB4xGEjTM6f1eHXBDguQcNvFasWIY6SrDbzaebmra-JHEABoCEBoQAvD_BwE
    # [DNS].opcode= Query  and [DNSQR].qtype = 1 - is type A meaaning Address Mapping record
    if (DNS in packet and packet[DNS].opcode == 0 and
        DNSQR in packet and packet[DNSQR].qtype == 1 and
        packet.haslayer("DNS Resource Record")):
        # packet.show()
        global googolIP
        googolIP = packet[DNS]["DNS Resource Record"].rdata
        return True
    else:
        return False

send_dns("google.co.il")
# print the DNS
print("start sniff 10 sec")
sniff(lfilter=filter_dns, prn=print_query_name, timeout=10)
