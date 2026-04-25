import socket
import ssl
import threading
import secrets

def create_secure_server(host='0.0.0.0', port=8000):
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
        # Generate a secure random token for each session
        session_token = secrets.token_hex(32)
        
        # Send the token to the client
        client_socket.sendall(f"Session token: {session_token}".encode('utf-8'))
        
        # Handle client requests here
        # ...
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    create_secure_server()