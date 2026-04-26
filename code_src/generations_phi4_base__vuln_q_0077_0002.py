import pickle
   import socket

   # Serialize data
   data_to_send = {'key': 'value', 'list': [1, 2, 3]}
   serialized_data = pickle.dumps(data_to_send)

   # Send data over a socket
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.connect(('hostname', port))
       s.sendall(serialized_data)

   # Receive data
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.bind(('hostname', port))
       s.listen()
       conn, addr = s.accept()
       with conn:
           received_data = conn.recv(1024)
           deserialized_data = pickle.loads(received_data)
           print(deserialized_data)

# ===== cell separator =====

import json
   import socket

   # Serialize data
   data_to_send = {'key': 'value', 'list': [1, 2, 3]}
   serialized_data = json.dumps(data_to_send).encode('utf-8')

   # Send data over a socket
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.connect(('hostname', port))
       s.sendall(serialized_data)

   # Receive data
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.bind(('hostname', port))
       s.listen()
       conn, addr = s.accept()
       with conn:
           received_data = conn.recv(1024)
           deserialized_data = json.loads(received_data.decode('utf-8'))
           print(deserialized_data)