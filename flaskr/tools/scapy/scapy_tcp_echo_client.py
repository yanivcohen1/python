from scapy. all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
# wireshark filter: ip.src == 104.70.125.117 or ip.dst == 104.70.125.117
# from Week16 tcp_echo_client.py
# https://gist.github.com/richarddun/1bb11d32cafc394efbcb8f4a8b6cb130
# url to ip4: https://www.nslookup.io/website-to-ip-lookup/

SERVER = "192.168.0.155" #"142.250.191.46 #google" #  # "manager1: python3 tcp_echo_client.py"
PORT = 5000 # 50

def stopfilter(x):
    if IP in x and x[IP].src == SERVER:  # src_ip
        return True
    else:
        return False

getStr = 'GET / HTTP/1.1\r\nHost:' + SERVER + '\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
while True:
    msg = input("send server a msg:")
    if msg == "stop":
        break
    if msg == "":
        msg = "TIME"

    #SEND SYN
    syn = IP(dst=SERVER) / TCP(sport=random.randint(1025,65500), dport=PORT, flags='S')
    #GET SYNACK
    syn_ack = sr1(syn)
    #Send ACK with the HTTP GET
    sr1(IP(dst=SERVER) / TCP(dport=PORT, sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack,
                                        ack=syn_ack[TCP].seq + 1, flags='A') / msg)

    ans = sniff(filter="tcp port " + str(PORT), stop_filter=stopfilter)
    # a.res[0]["IP"].show()
    # print(a.res[0]["IP"][Raw].load)
    for packet in ans:
        if packet.getlayer(Raw):
            l = packet.getlayer(Raw).load
            rawr = Raw(l)
            # rawr.show()
            print("client rcv payload: " + l.decode())
