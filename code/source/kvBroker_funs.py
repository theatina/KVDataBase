import re 
import argparse
import itertools
import random
import time
from datetime import datetime
import numpy as np
import string
import os
from subprocess import call
import threading
import socket
import customExceptions as ce 


def input_check(args):
    
    try:
        if not os.path.exists(args.s):
            raise ce.UsrInputError(f"\nERROR: File '{args.s}' does not exist!!\n") 
        if not os.path.exists(args.i):
            raise ce.UsrInputError(f"\nERROR: File '{args.i}' does not exist!!\n") 
        if args.k < 1:
            raise ce.UsrInputError(f"\nERROR: Server number must be > 0 ( '{args.k}' value was given )\n")

    except ce.UsrInputError as err:
        print(err.args[0])
        exit()


def arg_parsing(serverFile_path,dataToIndex_path):
    
    # Command: kvBroker -s serverFile.txt -i dataToIndex.txt -k 2    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default=serverFile_path, help=" Server ip-port list ")
    parser.add_argument("-i", type=str, default=dataToIndex_path, help=" Data ")
    parser.add_argument("-k", type=int, default=2, help=" Pick random k servers ")
    args = parser.parse_args()
    input_check(args)

    return args.s,args.i,args.k


def read_file(filepath):
    data = open(filepath,"r",encoding="utf-8").read()
    data = re.sub(r"\n\s+","\n",data)
    data = re.sub(r"\n$","",data)
    data = data.split("\n")

    return data

    # return [ elem for elem in open(filepath,"r",encoding="utf-8").read().split("\n") if elem!=r"\s+" ]




def thread_fun(ip,port):
    call(["python3", "kvServer.py", "-a", ip, "-p", port])

def server_connection(serverFile_path):
    servers = read_file(serverFile_path)
    server_ip_port = [ (ip_port.split(" ")[0],ip_port.split(" ")[1]) for ip_port in servers]
    # print(server_ip_port)
    # kvServer -a ip_address -p port
    

    threads = []
    for ip,port in server_ip_port:
        threads.append(threading.Thread(target=thread_fun,args=(ip,port)))

    # threads_exited = False
    # for th in threads:
    #     th.start()
    #     th.join(0.1)
    #     threads_exited = True

    return len(server_ip_port),threads


def server_sock_connection(server_list):
    sock_list = []
    for i,server in enumerate(server_list):
        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock_list[i].connect((server_list[i]._args[0], int(server_list[i]._args[1])))

    return sock_list

def server_request(sock_list,command):
    command = command.encode()
    for sock in sock_list:
        sock.sendall(command)
        data = sock.recv(2048)
        data_str = data.decode()



def send_data(server_threads,data,total_server_num,k_rand_servers,sock_list):

    server_ids_to_request = random.sample(range(0,total_server_num),k_rand_servers)
    print(server_ids_to_request)
    print(data)
    for row in data:
        command_data_sep = " "

        command_to_send = 'PUT ' + command_data_sep + row
        server_request(sock_list, command_to_send)

def server_exit_request(socket_list):
    for sock in socket_list:
        sock.sendall(b"exit")
        data = sock.recv(2048)
        data_str = data.decode()
        if data_str=="RIP":
            # print(sock.getpeername())
            print(f"\nServer {sock.getpeername()[0]}:{sock.getpeername()[1]} left the chat")


def query_time(sock_list,k_rand_servers):
    running = True
    while running:
        user_input = input("\nInsert Query: ")
        if user_input=="exit":
            # extra guard
            running = False
            break

        command = user_input.split(" ")[0]
        server_request(sock_list,command)

    server_exit_request(sock_list)
    # for sock in sock_list:
    #     sock.shutdown(socket.SHUT_RDWR)
    #     sock.close()
        




# def request_servers(server_list,command,server_threads):
#     command = command.encode()
    
#     for server in server_list:
#         if server_threads[server].is_alive:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.connect((server_threads[server]._args[0], int(server_threads[server]._args[1])))
#                 # command_to_send = command.encode("ascii")
#                 s.sendall(command)
#                 data = s.recv(2048)
#                 data_str = data.decode()
#                 # s.close
#                 # s.shutdown(socket.SHUT_RDWR)

#         print(f"Received {data_str} ")    
