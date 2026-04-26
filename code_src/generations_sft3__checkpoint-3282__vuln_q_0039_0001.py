import socket
import sys

def create_server(host='0.0.0.0', port=8888):
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set socket options to allow multiple connections
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to a specific address and port
        server_address = (host, port)
        sock.bind(server_address)
        
        # Listen for incoming connections (max 1 queued connection)
        sock.listen(1)
        
        print(f"Server is listening on {server_address}")
        
        while True:
            # Wait for a connection
            print("Waiting for a connection...")
            client, client_address = sock.accept()
            
            try:
                print(f"Connection from {client_address}")
                
                # Handle the client connection
                handle_client(client)
                
            finally:
                # Clean up the connection
                client.close()
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        sock.close()

def handle_client(client):
    try:
        while True:
            # Receive data from the client (max 1024 bytes)
            data = client.recv(1024)
            
            if not data:
                break
                
            # Send back the same data
            client.sendall(data)
            
    except Exception as e:
        print(f"Error handling client: {e}", file=sys.stderr)
    finally:
        client.close()

if __name__ == '__main__':
    create_server()