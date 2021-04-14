#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import kvServer_funs as kvsf
import trie as tr
import argparse
import socket
import server_generator as sg


data_filepath = "../data/"

# Command: kvServer -a ip_address -p port
parser = argparse.ArgumentParser()
parser.add_argument("-a", type=str, default="127.0.0.1")
parser.add_argument("-p", type=int, default=65430)
args = parser.parse_args()


ip = args.a
port = int(args.p)

# Root node of the trie structured server database
trie_server_dict = tr.Trie_Node(".")

# creates a server instance and starts it
s = sg.Server_Generator(ip,port,trie_server_dict)
s.startserver(trie_server_dict)
