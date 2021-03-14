#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'      # The server's hostname or IP address
PORT = 65432           # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'exit, world')
    data = s.recv(1024)
    data_str = data.decode()

print(f"Received {data_str} ")