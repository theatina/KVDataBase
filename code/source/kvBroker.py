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

serverFile_path,dataToIndex_path,k_rand_servers = kvbf.arg_parsing(serverFile_path,dataToIndex_path)

data = kvbf.read_file(dataToIndex_path)
# trie_dictionary = tr.Trie_Node(".")
print(data)
exit()
total_server_num,server_threads = kvbf.server_connection(serverFile_path)

threads_exited = False
for th in server_threads:
    th.start()
    th.join(0.1)
    threads_exited = True
    

kvbf.send_data(server_threads,data,total_server_num,k_rand_servers)

