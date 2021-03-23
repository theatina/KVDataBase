#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
 
Christina-Theano Kylafi
M111 - Big Data
LT1200012

'''

import re
import trie as tr

def CHECK_query(data,trie_server_dict):
    print(f"\nServer Check\n")
    print(f"Data: {data}")
    pass

def silly_tokenizer(data):
    temp_data_dict = {}
    data = data.split(" ")
    print(data)
    exit()


    return data

def PUT_query(data,trie_server_dict):
    print(f"\nPUT request\n")
    print(f"Data: {data}")

    top_level_key = data.split(":",maxsplit=1)[0]
    # top_level_key = re.findall(r"\"([a-zA-Z\d]+)\"",data[0])
    top_level_key = re.sub(r"\"","",top_level_key)
    # top_level_key = top_level_key.rstrip("\'")
    print(f"Top level key: {top_level_key}")

    # exit()
    print(data)

    tr.trie_insert_key(trie_server_dict,top_level_key,data,True)
    
    
    # tr.trie_delete_key(trie_server_dict,top_level_key)
    # temp_data_dict = silly_tokenizer(data)
    # # print(temp_data_dict)
    # out1,out2,key_node = tr.trie_find_key(trie_server_dict, "adfadf")
    # if key_node!=None:
    #     print(key_node.word,key_node.value,key_node.value_type)
    # else:
    #     print(out1,out2)

    pass


def GET_query(data,trie_server_dict):
    print(f"\nGET request\n")
    print(f"Data: {data}")
    
    # GET key
    # searches the nested keys and the keypaths(if the top level key is the desired) to create the data row

    # Get keypath
    # searches for the last key of the path and its respective keypath dictionary to get the value of the certain keypath if it exists
    
    pass

def DELETE_query(data,trie_server_dict):
    print(f"\nDELETE request\n")
    print(f"Data: {data}")
    pass

def QUERY_query(data,trie_server_dict):
    print(f"\nQUERY request\n")
    print(f"Data: {data}")
    pass