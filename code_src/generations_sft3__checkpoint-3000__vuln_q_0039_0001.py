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
            connection, client_address = sock.accept()
            
            try:
                print(f"Connection from {client_address}")
                
                # Receive data from the client (max 1024 bytes)
                amount_received = 0
                amount_expected = 1024
                
                while amount_received < amount_expected:
                    data = connection.recv(1024)
                    amount_received += len(data)
                    print(f"Received: {data.decode('utf-8')}")
                
                # Send response
                response = "Thank you for connecting"
                connection.sendall(response.encode('utf-8'))
                
            finally:
                # Clean up the connection
                connection.close()
                print("Connection closed")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    create_server()