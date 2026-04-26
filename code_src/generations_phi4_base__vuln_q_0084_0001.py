import socket

import threading


def handle_client(client_socket):

    request = client_socket.recv(1024)

    print(f"[*] Received: {request.decode('utf-8')}")

    client_socket.send(b"ACK")

    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('0.0.0.0', 9999))

server.listen(5)

print("[*] Listening on 0.0.0.0:9999")


while True:

    client, addr = server.accept()

    print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

    client_handler = threading.Thread(target=handle_client, args=(client,))

    client_handler.start()

# ===== cell separator =====

import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('0.0.0.0', 9999))

client.send(b"Hello, Server!")

response = client.recv(4096)

print(f"[*] Received: {response.decode('utf-8')}")

client.close()