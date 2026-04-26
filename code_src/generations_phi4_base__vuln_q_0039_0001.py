import socket
import threading

def handle_client(client_socket):
    with client_socket:
        print("Client connected:", client_socket.getpeername())
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
            client_socket.sendall(data)
        print("Client disconnected:", client_socket.getpeername())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))  # Bind to all available interfaces
    server.listen(5)
    print("Server listening on all interfaces...")

    while True:
        client_socket, addr = server.accept()
        print("Accepted connection from:", addr)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()