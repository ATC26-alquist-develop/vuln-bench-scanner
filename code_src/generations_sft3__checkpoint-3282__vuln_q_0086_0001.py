import socket
import threading
import ssl

def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_server(host='0.0.0.0', port=8888):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        
        while True:
            try:
                client_socket, addr = s.accept()
                with context.wrap_socket(client_socket, server_side=True) as secure_socket:
                    print(f"New connection from {addr}")
                    client_thread = threading.Thread(target=handle_client, args=(secure_socket, addr))
                    client_thread.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    start_server()