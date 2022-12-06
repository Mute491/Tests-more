import scapy.layers.l2 as scapyl2
import scapy.all as scapy
import os
import subprocess
import socket
import ipaddress
import platform

class Npire:

    def __init__(self):
        self.port_min = 0
        self.port_max = 65535
        self.address = ""
        self.subnet_mask = 0
        self.no_ping_response = False

        if (platform.system().lower() == "windows"):
            self.is_windows = True
            self.argument = "-n"
        else:
            self.is_windows = False
            self.argument = "-c"
        

    def get_parameters(ind, cmd):
        i = ind
        length = len(cmd)
        param = ""
        while i < length and cmd[i] != "-":
            param += cmd[i]
            i += 1

        try:
            return int(param)

        except:
            return -1


    def set_address(self, address):
        try:
            self.address = str(ipaddress.ip_address(address))
            return True
        except ValueError:
            return False


    def send_arp_request(self):
        arp_request = scapy.ARP(pdst=str(self.address))
        broadcast = scapyl2.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = broadcast / arp_request
        answered_list = scapy.srp(arp, timeout=2, verbose=False)[0]
        for element in answered_list:
                   #IP              MAC
            return element[1].psrc, element[1].hwsrc


    def network_scan_ping(self, start_index=0, end_index=0):

        available_hosts = []

        ip_list = list(ipaddress.ip_network(self.address + "/" + str(self.subnet_mask)).hosts())
        if end_index == 0:
            end_index=len(ip_list)
        ip_list = ip_list[start_index:end_index]

        try:

            for ip in ip_list:

                ip = str(ip)
                if subprocess.call(["ping", self.argument, "2", ip],
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT) == 0:
                    available_hosts.append(ip)

        except KeyboardInterrupt:
            pass

        return available_hosts

    def network_scan_arp(self, start_index=0, end_index=0):

        ip_list = list(ipaddress.ip_network(self.address + "/" + str(self.subnet_mask)).hosts())
        if end_index == 0:
            end_index=len(ip_list)
        ip_list = ip_list[start_index:end_index]

        available_hosts_ip = []
        available_hosts_mac = []

        try:

            for ip in ip_list:
                arp_request = scapy.ARP(pdst=str(ip))
                broadcast = scapyl2.Ether(dst="ff:ff:ff:ff:ff:ff")
                arp = broadcast / arp_request
                answered_list = scapy.srp(arp, timeout=2, verbose=False)[0]
                for element in answered_list:
                    available_hosts_ip.append(element[1].psrc)
                    available_hosts_mac.append(element[1].hwsrc)

        except KeyboardInterrupt:
            pass

        return available_hosts_ip, available_hosts_mac 


    def host_scan(self, range_min, range_max, protocol):

        ports_open = []
        services = []

        hostname = None
        if not(self.no_ping_response):
            hostname = socket.gethostbyaddr(self.address)

        protocol = protocol.lower()

        if protocol == "udp":
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for port in range(range_min, range_max):
                    data="111" 
                    s.sendto(data.encode(),(self.address,port))
                    s.settimeout(2)
                    try:
                        s.recvfrom(1024)
                        ports_open.append(port)
                        services.append(socket.getservbyport(port, protocol))
                    except:
                        pass

            except KeyboardInterrupt:
                pass

        elif protocol == "tcp":
            try:
                for port in range(range_min, range_max):
                    try:
                        print(port)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(2)
                        s.connect((self.address, port))
                        s.close()
                        ports_open.append(port)
                        services.append(socket.getservbyport(port, protocol))
                    except:
                        pass
            except KeyboardInterrupt:
                pass
               #open ports services names hostname
        return ports_open, services, hostname
