#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
 
Christina-Theano Kylafi
M111 - Big Data
LT1200012

'''

import re
import trie as tr

def check_query(data,trie_server_dict):
    print(f"\nServer Check\n")
    print(f"Data: {data}")
    pass

def PUT_query(data,trie_server_dict):
    print(f"\nPUT request\n")
    print(f"Data: {data}")

    top_level_key = data.split(":",maxsplit=1)[0]
    # top_level_key = re.findall(r"\"([a-zA-Z\d]+)\"",data[0])
    top_level_key = re.sub(r"\"","",top_level_key)
    # top_level_key = top_level_key.rstrip("\'")
    print(f"Top level key: {top_level_key}")
    # exit()
    # print(data_nested)

    # tr.trie_insert_key(trie_server_dict, )

    pass

def GET_query(data,trie_server_dict):
    print(f"\nGET request\n")
    print(f"Data: {data}")
    pass

def DELETE_query(data,trie_server_dict):
    print(f"\nDELETE request\n")
    print(f"Data: {data}")
    pass

def QUERY_query(data,trie_server_dict):
    print(f"\nQUERY request\n")
    print(f"Data: {data}")
    pass