#!/usr/bin/env python3

import os
import threading
import socket
import server_generator as sg

data_filepath = "../data/"

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#            conn.sendall(data)

server_filename = "serverFile.txt"
server_file_path = os.path.join(data_filepath,server_filename)

ip_ports_file_lines = open(server_file_path,"r",encoding="utf-8").read().split("\n")
id_ip_port_list = [ (id_num+1,line.split(" ")) for id_num,line in enumerate(ip_ports_file_lines)]

server_list = []
for server_info in id_ip_port_list:
    # print(server_info)
    id_num = server_info[0]
    ip_addr = server_info[1][0]
    port = int(server_info[1][1])
    s = sg.Server_Generator(ip_addr,port,id_num)
    server_list.append(s)

# server1 = sg.Server_Generator('127.0.0.1',65432,1)
# # server1.startserver()

# server2 = sg.Server_Generator('127.0.0.1',65431,2)
# # server2.startserver()

# server_list = [server1,server2]
threads = []
for server in server_list:
    threads.append(threading.Thread(target=server.startserver))


threads_exited = False
for th in threads:
    th.start()
    th.join(0.1)
    threads_exited = True

for i,server in enumerate(server_list):
    if threads[i].is_alive:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server.ip, server.port))
            s.sendall(b'exit, world')
            data = s.recv(1024)
            data_str = data.decode()

        print(f"Received {data_str} ")

# if threads_exited:
#     for server in server_list:
#         server.socket.close()