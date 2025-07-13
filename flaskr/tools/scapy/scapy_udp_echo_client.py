from scapy. all import *
from scapy.layers.inet import UDP, TCP, IP, Ether
# wireshark filter: ip.src == 104.70.125.117 or ip.dst == 104.70.125.117
# week18 udp_echo_client.py and udp_echo_server.py
SERVER = "192.168.1.155" # "52.42.3.50"  # "ynet.co.il"
PORT = 2000 # 201


def stopfilter(x):
    if IP in x and x[IP].src == SERVER:  # src_ip
        return True
    else:
        return False

syn_ip = IP(dst=SERVER)  # enter your ip's here
syn_syn = UDP(dport=PORT)

while True:
    msg = input("send server a msg:")
    if msg == "stop":
        break
    send(syn_ip/syn_syn/msg, verbose=0)
    ans = sniff(filter="udp port " + str(PORT),
                stop_filter=stopfilter, timeout=2)
    # ans.res[0]["IP"].show()
    # print(ans.res[0]["IP"][Raw].load)
    for packet in ans:
        if packet.getlayer(Raw):
            l = packet.getlayer(Raw).load
            rawr = Raw(l)
            # rawr.show()
            print("client rcv payload: " + l.decode())
