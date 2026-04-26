import socket

import threading


def handle_client(client_socket):

    with client_socket as sock:

        request = sock.recv(1024)

        print(f"[*] Received: {request.decode('utf-8')}")

        sock.send(b"ACK")

        sock.close()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('0.0.0.0', 9999))  # Bind to all interfaces on port 9999

    server.listen(5)  # Max number of queued connections

    print("[*] Listening on 0.0.0.0:9999")


    while True:

        client_sock, address = server.accept()

        print(f"[*] Accepted connection from {address[0]}:{address[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_sock,))

        client_handler.start()


if __name__ == "__main__":

    main()