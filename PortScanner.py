import scapy.layers.l2 as scapyl2
import scapy.all as scapy
import os
import subprocess
import socket
import ipaddress
import platform
import threading


# FUNZIONI


def get_parameters(ind, cmd):

    i = ind
    length = len(cmd)
    param = ""
    while i < length and cmd[i] != "-":
        param += cmd[i]
        i+=1

    try:
        return int(param)

    except:
        return -1


def is_address_valid(address):

    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def host_is_up(host):

    return subprocess.call(["ping", argument, "2", host], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT) == 0

def send_arp_request(address):
    arp_request = scapy.ARP(pdst=str(address))
    broadcast = scapyl2.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = broadcast / arp_request
    answered_list = scapy.srp(arp, timeout=2, verbose=False)[0]
    print("[*] Ip: " + answered_list[1].psrc)
    print("    Mac: " + answered_list[1].hwsrc)

def network_scan2(start_index, end_index):
    ip_list = list(network.hosts())
    ip_list = ip_list[start_index:end_index]

    for address in ip_list:

        address = str(address)

        if subprocess.call(["ping", argument, "2", address], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT) == 0:

            print("[*] " + address)


def network_scan(start_index, end_index):
    
    ip_list = list(network.hosts())
    ip_list = ip_list[start_index:end_index]

    for address in ip_list:
        arp_request = scapy.ARP(pdst=str(address))
        broadcast = scapyl2.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = broadcast/arp_request
        answered_list = scapy.srp(arp, timeout=2, verbose=False)[0]
        for element in answered_list:
            print("[*] Ip: " + element[1].psrc)
            print("    Mac: " + element[1].hwsrc)


def host_scan(ip, range_min, range_max):

    for port in range(range_min, range_max):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.close()
            print("[*] Port: %s => %s" %(port, socket.getservbyport(port, 'tcp')))
        except:
            pass



def print_help():
    print("COMANDI:")
    print("scan # serve a mostrare quali porte aperte ha l'host (utilizzabile con i parametri '--min' e '--max')")
    print("ping # serve a verificare se un host è online o no")
    print("network-scan # serve a scoprire quali host sono presenti nella rete e richiede i permessi di amministratore (utilizzabile con il parametro --subnet-mask)")
    print("network-scan2 # serve a scoprire quali host sono presenti nella rete e NON richiede i permessi di amministratore (utilizzabile con il parametro --subnet-mask)")
    print("\nPARAMETRI:")
    print("--address # va utilizzato alla fine di ogni comando per specificare l'host su cui eseguire il comando "
          "(es: ping --address 127.0.0.1 oppure scan --min 0 --max 10 --host 127.0.0.1)")
    print("--min # va utilizzato se si vuole indicare da quale porta deve iniziare lo scan (es: scan --min 0 --address 127.0.0.1)")
    print("--max # va utilizzato se si vuole indicare a quale porta deve terminare lo scan (es: scan --max 65535 --address 127.0.0.1)")
    print("--subnet-mask # va utilizzato per specificare la subnet mask della rete su cui si vuole eseguire lo scan (es: network-scan --subnet-mask 24 --address 192.168.1.0)")

# MAIN


if (platform.system().lower() == "windows"):
    argument = "-n"
else:
    argument = "-c"

port_min = 0
port_max = 65535

host_ip = ""
subnet_mask = 0

flag = True
no_ping_response = False

print("[ATTENZIONE] Usare il comando help per la guida\n")
command = input(">>>")
command = command.replace(" ", "")

# per uscire dal programma bisogna usare il comando exit
while command != "exit":

    # Controlla se è stato inserito il parametro address e se sì controlla che sia valido
    index = command.find("--address", 4)
    if index != -1:
        if not (is_address_valid(command[index + 9:])):
            flag = False

            print("[ERRORE] Indirizzo specificato in modo errato")
        else:
            host_ip = command[index+9:]

    # Controlla se è stato inserito il parametro min e se sì controlla che sia valido

    index = command.find("--min", 4)

    if index != -1:

        port_min = get_parameters(index + 5, command)

        if port_max == -1:
            flag = False

            print("[ERRORE] Parametro 'min' specificato in modo errato")

    # Controlla se è stato inserito il parametro max e se sì controlla che sia valido

    index = command.find("--max", 4)

    if index != -1:

        port_max = get_parameters(index + 5, command)

        if port_max == -1:
            flag = False

            print("[ERRORE] Parametro 'max' specificato in modo errato")

    # Controlla se è stato inserito il parametro subnet-mask e se sì controlla che sia valido

    index = command.find("--subnet-mask", 4)

    if index != -1:

        subnet_mask = get_parameters(index + 13, command)

        if port_max == -1:
            flag = False
            print("[ERRORE] Parametro 'max' specificato in modo errato")

    if command.find("--no-ping-response") != -1:
        no_ping_response = True

    # verifica se il comando digitato è help

    if command[0:4] == "help":
        print_help()

    # verifica se il comando digitato è ping

    elif command[0:3] == "arp":
        send_arp_request(host_ip)

    elif command[0:4] == "ping" and flag:

        # esecuzione comando
        if(host_is_up(host_ip)):
            print("[+] L'host è online")
        else:
            print("[-] L'host è offline")

    # verifica se il comando digitato è scan
    elif command[0:4] == "scan" and flag:

        # esecuzione comando

        is_valid = True

        try:
            if not no_ping_response:
                print(socket.gethostbyaddr(host_ip))

            print("[*] Inizio scansione dell'host")
        except:
            print("[ERRORE] Indirizzo non valido o l'host non è online")
            is_valid = False

        port_min -= 1
        port_max += 1

        if is_valid:

            # se bisogna controllare da 100 porte in poi il programma avvia 4 sotto processi per la ricerca
            if (port_max - port_min) >= 100:
                try:
                    temp = port_max // 4

                    thread = threading.Thread(target=host_scan, args=(host_ip, port_min, temp,))
                    thread_one = threading.Thread(target=host_scan, args=(host_ip, temp, temp + temp,))
                    thread_two = threading.Thread(target=host_scan, args=(host_ip, temp + temp, temp + temp + temp,))
                    thread_three = threading.Thread(target=host_scan, args=(host_ip, temp + temp + temp, port_max,))
                    thread.start()
                    thread_one.start()
                    thread_two.start()
                    thread_three.start()
                    thread.join()
                    thread_one.join()
                    thread_two.join()
                    thread_three.join() # l'esecuzione si ferma finchè il thread 3 non si ferma

                except:
                    thread.stop()
                    thread_one.stop()
                    thread_two.stop()
                    thread_three.stop()

            else:
                host_scan(host_ip, port_min, port_max)

    # verifica che il comando digitato è network-scan2
    elif command[0:13] == "network-scan2" and flag:
        try:
            network = ipaddress.ip_network(host_ip + "/" +str(subnet_mask))

            combinations = 2 ** (32 - subnet_mask) - 1
            temp = combinations // 6
            print("[*] I seguenti host sono online:")
            thread = threading.Thread(target=network_scan2, args=(0, temp,))
            thread_one = threading.Thread(target=network_scan2, args=(temp+1, temp+temp,))
            thread_two = threading.Thread(target=network_scan2, args=(temp+temp+1, temp*3))
            thread_three = threading.Thread(target=network_scan2, args=(temp*3+1, temp*4,))
            thread_four = threading.Thread(target=network_scan2, args=(temp*4+1, temp*5,))
            thread_five = threading.Thread(target=network_scan2, args=(temp*5+1, combinations,))
            thread.start()
            thread_one.start()
            thread_two.start()
            thread_three.start()
            thread_four.start()
            thread_five.start()
            thread.join()
            thread_one.join()
            thread_two.join()
            thread_three.join()
            thread_four.join()
            thread_five.join()
            # l'esecuzione si ferma finchè tutti i thread non si fermano
        except:
            thread.stop()
            thread_one.stop()
            thread_two.stop()
            thread_three.stop()
            thread_four.stop()
            thread_five.stop()
            print("[ERRORE] Assicurarsi di aver fornito i dati richiesti in modo corretto")

    # verifica che il comando digitato è network-scan
    elif command[0:12] == "network-scan" and flag:
        try:
            network = ipaddress.ip_network(host_ip + "/" + str(subnet_mask))
            try:
                combinations = 2 ** (32 - subnet_mask) - 1
           	temp = combinations // 6
            	print("[*] I seguenti host sono online:")
            	thread = threading.Thread(target=network_scan, args=(0, temp,))
            	thread_one = threading.Thread(target=network_scan, args=(temp+1, temp+temp,))
            	thread_two = threading.Thread(target=network_scan, args=(temp+temp+1, temp*3))
            	thread_three = threading.Thread(target=network_scan, args=(temp*3+1, temp*4,))
            	thread_four = threading.Thread(target=network_scan, args=(temp*4+1, temp*5,))
            	thread_five = threading.Thread(target=network_scan, args=(temp*5+1, combinations,))
		thread.start()
            	thread_one.start()
            	thread_two.start()
            	thread_three.start()
            	thread_four.start()
            	thread_five.start()
            	thread.join()
            	thread_one.join()
            	thread_two.join()
            	thread_three.join()
            	thread_four.join()
            	thread_five.join()
            # l'esecuzione si ferma finchè tutti i thread non si fermano
            except:
                print("[ERRORE] Assicurati di avere i permessi di amministratore\nin caso non è possibile averli utilizzare il comando network-scan2")
        except:
            print("[ERRORE] Assicurarsi di aver fornito i dati richiesti in modo corretto")
	# In caso di errore tutti i threads si stopperanno 
	try:
		thread.stop()
            	thread_one.stop()
            	thread_two.stop()
           	thread_three.stop()
            	thread_four.stop()
            	thread_five.stop()
	except:
		pass
	
    flag = True

    port_min = 0
    port_max = 65535
    subnet_mask = 0

    command = input("\n>>>")
    command = command.replace(" ", "")

print("[*] Chiusura programma")
