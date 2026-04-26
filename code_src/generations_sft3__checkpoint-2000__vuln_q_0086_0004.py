import socket
import threading
import ssl

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process data here
            response = "Server received: " + data.decode('utf-8')
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"Server listening on {host}:{port}")
        
        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            while True:
                try:
                    client_socket, addr = secure_socket.accept()
                    print(f"New connection from {addr}")
                    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                    client_thread.start()
                except Exception as e:
                    print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all available interfaces
    PORT = 8443  # Use a well-known port
    start_server(HOST, PORT)