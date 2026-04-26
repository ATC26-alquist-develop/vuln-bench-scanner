import socket
import pickle

def start_server(host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                obj = pickle.loads(data)
                print(f'Received: {obj}')
                # You can also send a response back if needed
                response = f'Received: {obj}'
                conn.sendall(pickle.dumps(response))

if __name__ == "__main__":
    start_server()

# ===== cell separator =====

import socket
import pickle

def send_object(host='localhost', port=65432, obj=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        serialized_obj = pickle.dumps(obj)
        s.sendall(serialized_obj)
        response = s.recv(1024)
        print(f'Received: {response}')

if __name__ == "__main__":
    obj_to_send = {'key': 'value', 'number': 42}
    send_object(obj=obj_to_send)