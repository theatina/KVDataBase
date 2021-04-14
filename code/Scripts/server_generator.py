#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import re 
import socket
import threading
import sys
import kvServer_funs as kvsf
import customExceptions as ce
import trie as tr


class Server_Generator:
    ''' 
    server class that represents a server with its methods used to start/maintain/stop the connection and exit the thread 
    '''

    def __init__(self,ip,port,trie_server_dict):
        self.ip = ip
        self.port = port
        # TCP protocol
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # remedy for immidiate reuse of the port 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.settimeout(5)
        try:
            self.socket.bind((self.ip, self.port)) 
        except socket.error as err:
            print(f"\nERROR {err.args[0]}: {err.args[1]}")
            self.kill_thread(trie_server_dict)

        # server data 
        self.trie_dictionary = None

    def startserver(self,trie_server_dict):
        # print(f"\nServer: Hi, my ip is: {self.ip} and port: {self.port}")
        while True:
            # starts listening at the certain ip and port through the socket
            self.socket.listen()
            conn, addr = self.socket.accept()

            # starts receiving data from the Broker 
            with conn:
                print(f"Connected to {self.ip}:{self.port}")
                # first, the Broker sends the maximum size that the server might need to receive (max size of data row), in order to avoid data loss
                max_buff_size = 2048
                data = conn.recv(max_buff_size)
                data_str = data.decode()
                msg = "go_on"
                while data_str[-10:]!="#__DONE__#":
                    data_str+= conn.recv(max_buff_size).decode()
                # print(data_str[-4:])
                data_str = data_str[:-10]
                if "#__exit__#" in data_str:
                    # stops the connection, deleted the trie structured DB and exits
                    self.stop_server(conn)
                    self.kill_thread(trie_server_dict)

                max_buff_size = int(data_str)
                # print(max_buff_size)
                conn.sendall(b"OK")
                conn.sendall(b"#__DONE__#")

                while True:
                    # the server continues to receive queries till "exit" message is received 
                    data = conn.recv(max_buff_size)
                    data_str = data.decode()
                    # safe way to receive data from the socket
                    msg = "go_on"
                    while data_str[-10:]!="#__DONE__#":
                        data_str+= conn.recv(max_buff_size).decode()
                    # print(data_str[-4:])
                    data_str = data_str[:-10]

                    if not data:
                        break

                    if "#__exit__#" in data_str:
                        # stops the connection, deleted the trie structured DB and exits
                        self.stop_server(conn)
                        self.kill_thread(trie_server_dict)
                
                    try:
                        # here, the server splits the query that is received from the Broker, checks the command and performs the necessary actions/checks to store, retrieve and delete entries

                        data_row = data_str.split(" ",maxsplit=1)
                        
                        if len(data_row)<2:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                        
                        if "PUT" not in data_str:
                            data_row[1] = data_row[1].strip()
                        
                        command = data_row[0].strip()
                        response = " "
                        if command == "PUT":
                            kvsf.PUT_query(data_row[1],trie_server_dict)
                        elif command == "GET":
                            response = kvsf.GET_query(data_row[1],trie_server_dict)
                            response = re.sub("'", "", response)
                        elif command == "DELETE":
                            response = kvsf.DELETE_query(data_row[1],trie_server_dict)
                        elif command == "QUERY":
                            response = kvsf.QUERY_query(data_row[1],trie_server_dict)
                            response = re.sub("'", "", response)
                        else:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
  
                        data_to_send = response.encode()
                        conn.sendall(data_to_send)
                        conn.sendall(b"#__DONE__#")
                        
                    except ce.QueryError as err:
                        print(f"\nServer {self.ip}:{self.port} : {err.args[0]}")
                        conn.sendall(b"NO")
                        conn.sendall(b"#__DONE__#")
                    

    def stop_server(self,conn):
        print(f"\n{self.ip}:{self.port} : Bye Bye world..")
        conn.sendall(b"RIP")
        conn.sendall(b"#__DONE__#")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
       

    def kill_thread(self,trie_server_dict):
        tr.delete_trie(trie_server_dict)
        sys.exit()
            
            
