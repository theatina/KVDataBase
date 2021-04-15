#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import datetime
import json
import re
import trie as tr


def write_log(ip,port,msg):
    with open(f"../LogFiles/log_server{ip}:{port}.txt","a",encoding="utf-8") as writer:
        writer.write(f"{datetime.datetime.now()}: {msg}\n")

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


def PUT_query(data,trie_server_dict,ip,port):
    '''
    Transforms the data row (entry) into a dictionary and calls the "nested_trie()" function to insert the entry in the trie structure of the server (database)
    '''
    
    data_dict = json_to_dict(data)
    # nested trie
    tr.nested_trie(trie_server_dict, data_dict) 

    write_log(ip,port,f"PUT {list(data_dict.keys())[0]} : {list(data_dict.values())[0]}")
    
    return 9


def DELETE_query(key,trie_server_dict,ip,port):
    '''
    Deletes the top level key "key" from the server's trie structure (database) and returns the appropriate message to send it to the Broker as a response to the DELETE query
    '''
    
    key = re.sub("[\"']", "", key)
    success = tr.trie_delete_key(trie_server_dict, key)
    found_msg = "NOT FOUND"
    if success==9:
        found_msg = "OK"
        response="OK"
    else:
        response="NO"

    write_log(ip,port,f"DELETE {key} : {found_msg}")

    return response


def GET_query(data,trie_server_dict,ip,port):
    '''
    Top level key value retrieval - if the key is in the trie structure of the certain server
    '''
    
    data = re.sub("[\"']", "", data)
    data.rstrip(" ")
    data.lstrip(" ")
    
    key = data

    val_dict = {}
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, [key])

    found_msg = "NOT FOUND"
    if found:
        found_msg = val_dict
        response = f"{key} : {val_dict}"
    else:
        response=" "
    
    write_log(ip,port,f"GET {key} : {found_msg}")
    
    return response


def QUERY_query(data,trie_server_dict,ip,port):
    '''
    Returns the value (single value or set of key-value pairs) of the keypath given using the "trie_find_keypath_nested()" function of the trie structure described in "trie.py"
    '''
    
    key_path = data.split(".")
    for i,k in enumerate(key_path):
        key_path[i] = key_path[i].rstrip(" ")
        key_path[i] = key_path[i].lstrip(" ")
    
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, key_path)

    found_msg = "NOT FOUND"
    if found:
        found_msg = val_dict
        response = f"{'.'.join(key_path)} : {val_dict}"
    else:
        response=" "

    write_log(ip,port,f"QUERY {'.'.join(key_path)} : {found_msg}")

    return response