#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

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
from collections import Counter

def input_check(args):
    
    try:
        if not os.path.exists(args.s):
            raise ce.UsrInputError(f"\nERROR: File '{args.s}' does not exist!!\n") 
        if not os.path.exists(args.i):
            raise ce.UsrInputError(f"\nERROR: File '{args.i}' does not exist!!\n") 
        if args.k < 1:
            raise ce.UsrInputError(f"\nERROR: Server number must be > 0 ( '{args.k}' value was given )\n")
        
        with open(args.s,"r",encoding="utf-8") as reader:
            servers = len(reader.read().split("\n"))
            if args.k > servers:
                raise ce.UsrInputError(f"\nERROR: Random servers number({args.k}) must be <= total servers number({servers}) !!\n")

    except ce.UsrInputError as err:
        print(err.args[0])
        exit()


def arg_parsing(serverFile_path,dataToIndex_path):
    
    # Command: kvBroker -s serverFile.txt -i dataToIndex.txt -k 2    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default=serverFile_path, help=" Server ip-port list ")
    parser.add_argument("-i", type=str, default=dataToIndex_path, help=" Data to store")
    parser.add_argument("-k", type=int, default=2, help=" Pick random k servers ")
    args = parser.parse_args()
    input_check(args)

    return args.s,args.i,args.k


def read_file(filepath):
    data = open(filepath,"r",encoding="utf-8").read().strip().split("\n")
    return data


def thread_fun(ip,port):
    # kvServer -a ip_address -p port
    call(["python3", "kvServer.py", "-a", ip, "-p", port])

def server_connection(serverFile_path):
    servers = read_file(serverFile_path)
    server_ip_port = [ (ip_port.split(" ")[0],ip_port.split(" ")[1]) for ip_port in servers]
    

    threads = []
    for ip,port in server_ip_port:
        threads.append(threading.Thread(target=thread_fun,args=(ip,port)))


    return len(server_ip_port),threads


def server_sock_connection(server_list):
    sock_list = []
    for i,server in enumerate(server_list):
        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock_list[i].connect((server_list[i]._args[0], int(server_list[i]._args[1])))

    return sock_list

def server_sock_connection_check(sock_list,server_list):
    servers_down = 0

    for i,server in enumerate(server_list):

        server_dead = server.is_alive()==False
        if server_dead:
            servers_down+=1
        else:
            file_num = sock_list[i].fileno()
            if file_num==-1:
                servers_down+=1

    return servers_down



def server_request(sock_list,request,server_list,k_rand_servers):
    request = re.sub("\s+", " ", request)
    # request = request.lstrip(" ")
    # request = request.rstrip(" ")
    request_parts = request.strip().split(" ",maxsplit=1)

    for i,part in enumerate(request_parts):
        request_parts[i] = request_parts[i].strip(r"\s")
    
    command = request_parts[0]
    servers_down = server_sock_connection_check(sock_list,server_list)
    if len(request_parts)<2 and (any(query == command for query in ["DELETE","GET","QUERY"])==False):
        print(f"\nERROR: '{request_parts[0]}': Invalid syntax !\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return -9
    elif len(request_parts)<2:
        print(f"\nERROR: '{request_parts[0]}': Invalid syntax ! (missing arguments)\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return -9
    elif len(request_parts[1].split(" "))>1:
        print(f"\nERROR: '{' '.join(request_parts)}': Invalid syntax ! (too many arguments)\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return -9
    elif servers_down==len(server_list):
        print(f"\nFATAL ERROR: All servers are down!\n({servers_down} servers)")
        return -8
    elif any(query == command for query in ["DELETE","GET","QUERY"])==False:
        print(f"\nERROR: '{command}': Invalid query !\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return -9
    elif command == "DELETE" and servers_down:
        print(f"\nCannot perform DELETE query with >=1 servers down!")
        return -9
    elif (command == "GET" or command == "QUERY") and servers_down>=k_rand_servers:
        print(f"\nWARNING: {servers_down} servers are down! (Correct output is not guaranteed)")


    request_to_send = " ".join(request_parts).encode()
    responses = []
    for i,sock in enumerate(sock_list):
        if server_list[i].isAlive() and sock.fileno()!=-1:
            sock.sendall(request_to_send)
            data = sock.recv(2048)
            data_str = data.decode()

            responses.append(data_str)
            # In case we wanted to stop at the first server entry retrieval 
            # if data_str not in ["OK"," ","NO"]:
            #     break

    if len(responses)==0:
        return -9
    elif command == "DELETE" and "OK" in responses:
        print(f"\n'{command} {request_parts[1]}' completed successfully!")
    elif  command == "DELETE" and "OK" not in responses:
        print(f"\n'{command} {request_parts[1]}' failed!\n(key '{request_parts[1]}' not found or another problem occured)")
    elif responses.count(" ")==len(responses):
        print(f"\n'{request_parts[1]}' NOT FOUND")
    else:
        responses = [i for i in responses if i!=" " and i!="OK" and i!="NO"]
        if len(responses)==0:
            return -9
        else:
            diff_responses = Counter(responses).keys()
            if len(diff_responses)>1:
                print(f"\n{len(diff_responses)} different entries were retrieved:")
                for i,entry in enumerate(diff_responses):
                    print(f"\n{i+1}. {entry}")
            elif len(diff_responses)==1:
                print(f"\n{responses[0]}")

    return 9


def server_store(sock_list,request,sock_indices,max_buff_size):
    request = request.encode()
    for sock_ind in sock_indices:
        sock_list[sock_ind].sendall(request)
        data = sock_list[sock_ind].recv(max_buff_size)
        # data_str = data.decode()


def calculate_max_msg_size(data):
    max_real_size = max([len(row) for row in data])
    diff = 2**10-max_real_size
    counter = 10
    while diff<=0:
        min_diff = diff
        counter+=1
        diff = 2**counter-max_real_size


    # p_of_2_diff = [ 2**i-max_real_size if 2**i-max_real_size>0 else 0 for i in range(10,20)  ]
    p_of_2_size = 2**counter 
    
    return p_of_2_size


def send_max_size(sock_list,server_list,max_buff_size):
    servers_down = server_sock_connection_check(sock_list,server_list)
    if servers_down==len(server_list):
        print(f"\nFATAL ERROR: All servers are down !!")
        server_exit_request(sock_list,server_list,max_buff_size)
        exit()
    
    max_size_to_send = str(max_buff_size).encode()
    for i,sock in enumerate(sock_list):
        if server_list[i].isAlive() and sock.fileno()!=-1:
            sock.sendall(max_size_to_send)
            # data = sock.recv(2048)
            # data_str = data.decode()


def send_data(server_threads,data,total_server_num,k_rand_servers,sock_list,max_buff_size):
    time.sleep(1)
    send_max_size(sock_list,server_threads,max_buff_size)
    
    print(f"\nStoring Data..\n")
    for i,row in enumerate(data):
        if i+1 in [len(data)//4,len(data)//3,len(data)//2,3*len(data)//4,len(data)]:
            print(f"{(i+1)*100//len(data)}% of the data is stored..")
        
        sock_indices = random.sample(range(0,total_server_num),k_rand_servers)
        command_data_sep = " "
        data_to_send = 'PUT' + command_data_sep + row
        server_store(sock_list,data_to_send,sock_indices,max_buff_size)
    


def server_exit_request(socket_list,server_list,max_buff_size):
    for i,sock in enumerate(socket_list):
        if server_list[i].isAlive() and sock.fileno()!=-1:
            sock.sendall(b"exit")
            data = sock.recv(max_buff_size)
            data_str = data.decode()
            if data_str=="RIP":
                print(f"\nServer {sock.getpeername()[0]}:{sock.getpeername()[1]} has left the chat\n")

    print(f"\nExiting..\n")

def query_time(sock_list,server_list,k_rand_servers,max_buff_size):
    running = True
    # sock_list[0].sendall(b"exit")
    # sock_list[1].sendall(b"exit")
    # sock_list[2].sendall(b"exit")

    while running:
        servers_down = server_sock_connection_check(sock_list,server_list)
        if servers_down==len(server_list):
            print(f"\nFATAL ERROR: All servers are down!\n({servers_down} servers)")
            server_exit_request(sock_list,server_list,max_buff_size)
            return -8

        user_input = input("\nInsert Query (type 'exit' to quit): ")
        if "exit" in user_input.lower():
            # extra guard
            running = False
            server_exit_request(sock_list,server_list,max_buff_size)
            return 9
        else:
            err_code = server_request(sock_list,user_input,server_list,k_rand_servers)
            if err_code==-8:
                server_exit_request(sock_list,server_list,max_buff_size)
                running = False
                return -9
           
                    