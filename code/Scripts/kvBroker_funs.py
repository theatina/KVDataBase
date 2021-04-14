#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import sys
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
    ''' 
    Performs the necessary checks on the command line arguments 
    '''

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
    ''' 
    Command line parser and checker
    '''
    
    # Command: kvBroker -s serverFile.txt -i dataToIndex.txt -k 2    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default=serverFile_path, help=" Server ip-port list ")
    parser.add_argument("-i", type=str, default=dataToIndex_path, help=" Data to store")
    parser.add_argument("-k", type=int, default=2, help=" Pick random k servers ")
    args = parser.parse_args()
    input_check(args)

    return args.s,args.i,args.k


def read_file(filepath):
    ''' 
    Reads the entry data file and returns the entry rows
    '''

    data = open(filepath,"r",encoding="utf-8").read().strip().split("\n")
    return data


def thread_fun(ip,port):
    ''' 
    The function that will instantiate the threads later, with the proper ip and port as arguments for each server
    '''

    # kvServer -a ip_address -p port
    call(["python3", "kvServer.py", "-a", ip, "-p", port])

def server_connection(serverFile_path):
    ''' 
    Instantiates the threads/servers included in the "serverFile_path" file using the function "thread_fun()" above and returns a list of all the threads
    '''

    servers = read_file(serverFile_path)
    server_ip_port = [ (ip_port.split(" ")[0],ip_port.split(" ")[1]) for ip_port in servers]
    

    threads = []
    for ip,port in server_ip_port:
        threads.append(threading.Thread(target=thread_fun,args=(ip,port)))
        threads[-1].setName(f"Server_{ip}:{port}")

    return len(server_ip_port),threads


def server_sock_connection(server_list,max_buff_size):
    ''' 
    Server connection establishing
    '''
    
    sock_list = []
    for i,server in enumerate(server_list):
        # TCP protocol
        sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    for i,server in enumerate(server_list):
        if server_list[i].is_alive() and sock_list[i].fileno()!=-1:
            # sock_list[i].settimeout(5)
            try:
                # establishing the connections
                sock_list[i].connect((server_list[i]._args[0], int(server_list[i]._args[1])))
            except socket.error as err:
                print(f"\nERROR {err.args[0]}: Problem with socket {i} ({err.args[1]})")
                return server_exit_request_emergency(sock_list,server_list)


    return sock_list


def server_sock_connection_check(sock_list,server_list):
    ''' 
    Runs thread/socket checks and counts the servers that are down to let the Broker know and perform the proper actions
    '''

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

def check_before_request(sock_list,request,server_list,k_rand_servers):
    '''
    Query checker in order to not send wrong queries to the servers or perform a DELETE query when a server is down and warn the user for an unreliable answer when k or more servers are down, etc.
    '''
    err_num = 9 #all good

    request = re.sub(r"\s+", " ", request)
    request_parts = request.strip().split(" ",maxsplit=1)

    for i,part in enumerate(request_parts):
        request_parts[i] = request_parts[i].strip(" ")
        request_parts[i] = request_parts[i].strip(r"\"")
        request_parts[i] = request_parts[i].strip(r"'")
    
    command = request_parts[0]
    # check how many servers are down, if any
    servers_down = server_sock_connection_check(sock_list,server_list)
    if len(request_parts)<2 and (any(query == command for query in ["DELETE","GET","QUERY"])==False):
        print(f"\nERROR: '{request_parts[0]}': Invalid syntax !\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return "",[],-9
    elif len(request_parts)<2:
        print(f"\nERROR: '{request_parts[0]}': Invalid syntax ! (missing arguments)\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return "",[],-9
    elif len(request_parts[1].split(" "))>1:
        print(f"\nERROR: '{' '.join(request_parts)}': Invalid syntax ! (too many arguments)\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return "",[],-9
    elif servers_down==len(server_list):
        print(f"\nFATAL ERROR: All servers are down!\n({servers_down} servers)")
        return "",[],-8
    elif any(query == command for query in ["DELETE","GET","QUERY"])==False:
        print(f"\nERROR: '{command}': Invalid query !\n\nSyntax: DELETE <top_level_key> | GET <top_level_key> | QUERY <top_level_key(.nested_key...nested_key)>")
        return "",[],-9
    elif command == "DELETE" and servers_down:
        print(f"\nCannot perform DELETE query with >=1 servers down!")
        return "",[],-9
    elif (command == "GET" or command == "QUERY") and servers_down>=k_rand_servers:
        print(f"\nWARNING: {servers_down} servers are down! (Correct output is not guaranteed)")


    return command, request_parts, err_num



def server_request(sock_list,request,server_list,k_rand_servers,max_buff_size):
    ''' 
    Makes requests to the servers after checking the query, receives their response, performs checks one more time and then outputs the proper error message or answer to the user
    '''

    command, request_parts, err_num = check_before_request(sock_list,request,server_list,k_rand_servers)

    if err_num!=9:
        return err_num

    request_to_send = " ".join(request_parts).encode()
    responses = []
    for i,sock in enumerate(sock_list):
        if server_list[i].is_alive() and sock.fileno()!=-1:
            sock.sendall(request_to_send)
            sock.sendall(b"#__DONE__#")

            data = sock.recv(max_buff_size)
            data_str = data.decode()
            # safe way to receive data from the socket
            msg = "go_on"
            while data_str[-10:]!="#__DONE__#":
                if server_list[i].is_alive() and sock.fileno()!=-1:
                    data_str+= sock.recv(max_buff_size).decode()
            # print(data_str[-4:])
            data_str = data_str[:-10]

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


def server_store(sock_list,server_list,request,sock_indices,max_buff_size):
    ''' 
    Stores an entry to k randomly picked servers and receives an ack that everything went well
    '''

    request = request.encode()
    for sock_ind in sock_indices:
        if server_list[sock_ind].is_alive() and sock_list[sock_ind].fileno()!=-1:
            sock_list[sock_ind].sendall(request)
            sock_list[sock_ind].sendall(b"#__DONE__#")
            data = sock_list[sock_ind].recv(max_buff_size)
            data_str = data.decode()
            # safe way to receive data from the socket
            msg = "go_on"
            while data_str[-10:]!="#__DONE__#":
                if server_list[sock_ind].is_alive() and sock_list[sock_ind].fileno()!=-1:
                    data_str+= sock_list[sock_ind].recv(max_buff_size).decode()


def calculate_buff_size(data):
    ''' 
    Randomly chooses a buffer size between 3 sizes (1024, 2048 and 4096)
    Just for fun!
    '''
    buff_size_rand = random.randint(0,2)
    sizes = [2**(10+i) for i in range(0,3)]

    return sizes[buff_size_rand]
    


def send_buff_size(sock_list,server_list,max_buff_size):
    ''' 
    Sends the buffer size chosen by the function above
    '''

    servers_down = server_sock_connection_check(sock_list,server_list)
    if servers_down==len(server_list):
        print(f"\nFATAL ERROR: All servers are down !!")
        server_exit_request(sock_list,server_list,max_buff_size)
        exit()
    
    max_size_to_send = str(max_buff_size).encode()
    for i,sock in enumerate(sock_list):
        if server_list[i].is_alive() and sock.fileno()!=-1:
            sock.sendall(max_size_to_send)
            sock.sendall(b"#__DONE__#")
            data = sock.recv(max_buff_size)
            data_str = data.decode()
            # safe way to receive data from the socket
            msg = "go_on"
            while data_str[-10:]!="#__DONE__#":
                data_str+= sock.recv(max_buff_size).decode()
            # print(data_str[-4:])
            data_str = data_str[:-10]

            if "OK" not in data_str:
                print(f"\nERROR: something went wrong with {server_list[i].getName}")
                print(f"\n!!KILLING {server_list[i].getName}")
                sock.sendall(b"#__exit__#")
                sock.sendall(b"#__DONE__#")
                


def send_data(server_threads,data,total_server_num,k_rand_servers,sock_list,max_buff_size):
    ''' 
    Function that sends/stores the data from the entry file by first checking if all servers are up, then sending them the maximum msg size that will be sent over the socket (not necessary in the latest version of the programme's implementation though) and finally sending the data entry by entry to k randomly picked servers
    '''

    # # testing with servers down
    # servers_to_kill = random.randint(0,len(server_threads)-3)
    # rand_servers = random.sample(range(0,len(server_threads)-1),servers_to_kill)
    # for i in rand_servers:
    #     print(f"\n!!KILLING {server_threads[i].getName()}!!")
    #     sock_list[i].sendall(b"#__exit__#")
    #     sock_list[i].sendall(b"#__DONE__#")
    #     time.sleep(0.9)

    servers_down = server_sock_connection_check(sock_list,server_threads)
    if servers_down==len(server_threads):
        print(f"\nFATAL ERROR: All servers are down !!")
        server_exit_request(sock_list,server_threads,max_buff_size)
        return -19

    time.sleep(1)
    send_buff_size(sock_list,server_threads,max_buff_size)
    
    print(f"\nStoring Data..\n")
    for i,row in enumerate(data):
        if i+1 in [len(data)//4,len(data)//3,len(data)//2,3*len(data)//4,len(data)]:
            print(f"{(i+1)*100//len(data)}% of the data is stored..")
        
        sock_indices = random.sample(range(0,total_server_num),k_rand_servers)
        command_data_sep = " "
        data_to_send = 'PUT' + command_data_sep + row
        server_store(sock_list,server_threads,data_to_send,sock_indices,max_buff_size)
    


def server_exit_request(socket_list,server_list,max_buff_size):
    ''' 
    Stops the servers by sending an exit message to those still running
    '''

    for i,sock in enumerate(socket_list):
        if server_list[i].is_alive() and sock.fileno()!=-1:
            sock.sendall(b"#__exit__#")
            sock.sendall(b"#__DONE__#")
            data = sock.recv(max_buff_size)
            data_str = data.decode()
            # safe way to receive data from the socket
            msg = "go_on"
            while data_str[-10:]!="#__DONE__#":
                data_str+= sock.recv(max_buff_size).decode()

            data_str = data_str[:-10]

            if data_str=="RIP":
                print(f"\nServer {sock.getpeername()[0]}:{sock.getpeername()[1]} has left the chat\n")



def query_time(sock_list,server_list,k_rand_servers,max_buff_size):
    ''' 
    Waits for user input till an "exit" request is received 
    '''

    running = True
    while running:
        servers_down = server_sock_connection_check(sock_list,server_list)
        if servers_down==len(server_list):
            print(f"\nFATAL ERROR: All servers are down!\n({servers_down} servers)")
            server_exit_request(sock_list,server_list,max_buff_size)
            return -8

        user_input = input("\n\nInsert Query (type 'exit' to quit): ")
        if "exit" in user_input.lower():
            # extra guard
            running = False
            server_exit_request(sock_list,server_list,max_buff_size)
            return 9
        else:
            err_code = server_request(sock_list,user_input,server_list,k_rand_servers,max_buff_size)
            if err_code==-8:
                server_exit_request(sock_list,server_list,max_buff_size)
                running = False
                return -9
           

def server_exit_request_emergency(sock_list,server_list):
    '''
    Emergency exit: stops the servers by sending an exit message to those still running (due to connection error)
    '''

    for i,sock in enumerate(sock_list):
        if server_list[i].is_alive() and sock.fileno()!=-1:
            try:
                error1 = sock.sendall(b"#__exit__#")
                error2 = sock.sendall(b"#__DONE__#")
                print(error1,error2)
            except socket.error as err:
                print(f"\nERORR {err.args[0]}: {err.args[1]}")
    
    return []