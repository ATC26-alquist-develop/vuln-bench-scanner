import socket
import sys

def create_server(host='', port=8888):
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to a specific address and port
        server_address = (host, port)
        sock.bind(server_address)
        
        # Listen for incoming connections (allow backlog of 1)
        sock.listen(1)
        
        print(f"Server is listening on {server_address}")
        
        while True:
            # Wait for a connection
            print("Waiting for a connection...")
            connection, client_address = sock.accept()
            
            try:
                print(f"Connection from {client_address}")
                
                # Receive the data in small chunks
                while True:
                    data = connection.recv(16)
                    if data:
                        print(f"Received: {data.decode('utf-8').strip()}")
                    else:
                        print("No more data from", client_address)
                        break
                
                # Send response
                response = "HTTP/1.1 200 OK\r\n\r\nHello, World!"
                connection.sendall(response.encode('utf-8'))
            
            finally:
                # Clean up the connection
                connection.close()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    create_server()