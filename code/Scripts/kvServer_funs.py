#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import json
import re
import trie as tr


def json_to_dict(data):
    '''
    Conversion of an entry into dictionary format using jason
    '''

    temp_data_dict = {}
    if data!="{}":
        if ";" in data:
            data = re.sub(";", ",", data)
        
        top_level_key,tlk_value = data.split(" : ", maxsplit=1)
        top_level_key = top_level_key.strip("\"")
        temp_data_dict[top_level_key] = json.loads(tlk_value)

    return temp_data_dict


def PUT_query(data,trie_server_dict):
    '''
    Transforms the data row (entry) into a dictionary and calls the "nested_trie()" function to insert the entry in the trie structure of the server (database)
    '''
    # print(data)
    data_dict = json_to_dict(data)
    # nested trie
    tr.nested_trie(trie_server_dict, data_dict) 
    
    return 9


def DELETE_query(key,trie_server_dict):
    '''
    Deletes the top level key "key" from the server's trie structure (database) and returns the appropriate message to send it to the Broker as a response to the DELETE query
    '''
    
    key = re.sub("[\"']", "", key)
    success = tr.trie_delete_key(trie_server_dict, key)
    if success==9:
        response="OK"
    else:
        response="NO"
    return response


def GET_query(data,trie_server_dict):
    '''
    Top level key value retrieval - if the key is in the trie structure of the certain server
    '''
    
    data = re.sub("[\"']", "", data)
    data.rstrip(" ")
    data.lstrip(" ")
    
    key = data

    val_dict = {}
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, [key])

    if found:
        response = f"{key} : {val_dict}"
    else:
        response=" "
    return response


def QUERY_query(data,trie_server_dict):
    '''
    Returns the value (single value or set of key-value pairs) of the keypath given using the "trie_find_keypath_nested()" function of the trie structure described in "trie.py"
    '''
    
    key_path = data.split(".")
    for i,k in enumerate(key_path):
        key_path[i] = key_path[i].rstrip(" ")
        key_path[i] = key_path[i].lstrip(" ")
    
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, key_path)

    if found:
        response = f"{'.'.join(key_path)} : {val_dict}"
    else:
        response=" "
    return response