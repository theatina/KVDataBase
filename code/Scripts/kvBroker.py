#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import os
import kvBroker_funs as kvbf
import trie as tr
import threading
import random

data_filepath = "../data"
dataToIndex_path =  os.path.join(data_filepath,"dataToIndex.txt")
serverFile_path =  os.path.join(data_filepath,"serverFile.txt")

# command line input parsing
serverFile_path,dataToIndex_path,k_rand_servers = kvbf.arg_parsing(serverFile_path,dataToIndex_path)

data = kvbf.read_file(dataToIndex_path)
total_server_num,server_threads = kvbf.server_connection(serverFile_path)

# starts the threads/servers
for th in server_threads:
    th.start()
    th.join(0.1)
    
# choose the buffer size of the socket data exchange over a socket (random pick just for fun)
max_buff_size = kvbf.calculate_buff_size(data)    
socket_list = kvbf.server_sock_connection(server_threads,max_buff_size)
# store the data
kvbf.send_data(server_threads,data,total_server_num,k_rand_servers,socket_list,max_buff_size)
# start making queries
kvbf.query_time(socket_list,server_threads,k_rand_servers,max_buff_size)


for th in server_threads:
    if th.is_alive():
        th.join()
    

exit()