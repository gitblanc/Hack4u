#!/usr/bin/env python3 
import socket
import threading
import ssl # para la comunicación cifrada

def client_thread(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\n[+] El usuario {username} se ha conectado al chat.")

    for client in clients: # para enivar el mensaje de que te has conectado al resto de usuarios
        if client is not client_socket:
            client.sendall(f"\n[+] El usuario {username} se ha conectado al chat.\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message == "!usuarios":
                client_socket.sendall(f"[+] Listado de usuarios conectados:\n {', '.join(usernames.values())}\n\n".encode())
                continue

            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]

def server_program():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TIME_WAIT
    server_socket.bind((host, port))
    # Para operar empleando comunicación cifrada y un certificado autofirmado
    server_socket = ssl.wrap_socket(server_socket, keyfile="server-key.key", certfile="server-cert.pem", server_side=True)
    server_socket.listen() # ponernos en escucha de conexiones entrantes

    print(f"\n[+] El servidor está en escucha de conexiones entrantes...")

    clients = []
    usernames = {}

    while True:
        client_socket, address = server_socket.accept() # se acepta el cliente
        clients.append(client_socket)

        print(f"\n[+] Se ha conectado un nuevo cliente: {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.daemon = True # si no pongo esto, si cierro el programa puede quedarse en espera y no concluya
        thread.start()

    server_socket.close()

if __name__ == '__main__':
    server_program()