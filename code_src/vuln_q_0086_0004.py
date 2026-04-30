import socket
import ssl
import threading
import logging

def create_secure_server(host='127.0.0.1', port=8888):
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Create a socket and wrap it with SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as secure_sock:
            while True:
                client, addr = secure_sock.accept()
                handle_client(client, addr)

def handle_client(client_socket, addr):
    try:
        # Handle client connection securely
        data = client_socket.recv(1024)
        if data:
            # Process data securely
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, secure world!"
            client_socket.send(response)
    except Exception as e:
        logging.error(f"Error handling client {addr}: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    create_secure_server()