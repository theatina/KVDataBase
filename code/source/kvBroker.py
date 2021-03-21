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

data_filepath = "../data"
dataToIndex_path =  os.path.join(data_filepath,"dataToIndex.txt")
serverFile_path =  os.path.join(data_filepath,"serverFile.txt")

serverFile_path,dataToIndex_path,k_rand_servers = kvbf.arg_parsing(serverFile_path,dataToIndex_path)

# data = kvbf.read_file(dataToIndex_path)
# print(data)

trie_dictionary = tr.Trie_Node(".")

tr.data_indexing_from_file(trie_dictionary, dataToIndex_path)