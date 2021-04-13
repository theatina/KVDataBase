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
import kvServer_funs as kvsf
import customExceptions as ce
import trie as tr

class Server_Generator:
    ''' 
    server class that represents a server with its methods used to start/maintain/stop the connection and exit the thread 
    '''

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port)) 

        # server data 
        self.trie_dictionary = None

    def startserver(self,trie_server_dict):
        # print(f"\nServer: Hi, my ip is: {self.ip} and port: {self.port}")
        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()

            with conn:
                print(f"Server with ip '{self.ip}' and port '{self.port}': connection established")
                max_buff_size = 2048
                data = conn.recv(max_buff_size)
                data_str = data.decode()
                max_buff_size = int(data_str)

                while True:
                    data = conn.recv(max_buff_size)
                    data_str = data.decode()

                    if not data:
                        break

                    if "exit" in data_str:
                        self.stop_server(conn)
                        self.kill_thread(trie_server_dict)
                
                    try:
                        data_row = data_str.split(" ",maxsplit=1)
                        
                        if len(data_row)<2:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                        
                        if "PUT" not in data_str:
                            data_row[1] = data_row[1].strip()
                            # data_row[1] = data_row[1].lstrip(" ")

                        
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
                        
                    except ce.QueryError as err:
                        print(f"\nServer {self.ip}:{self.port} : {err.args[0]}")
                        conn.sendall(b"NO")
                    

    def stop_server(self,conn):
        print(f"\n{self.ip}:{self.port} : Bye Bye world..")
        conn.sendall(b"RIP")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
       

    def kill_thread(self,trie_server_dict):
        tr.delete_trie(trie_server_dict)
        exit()
            
            
