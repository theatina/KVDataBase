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
    temp_data_dict = {}
    if data!="{}":
        if ";" in data:
            data = re.sub(";", ",", data)
        
        top_level_key,tlk_value = data.split(" : ", maxsplit=1)
        top_level_key = top_level_key.strip("\"")
        temp_data_dict[top_level_key] = json.loads(tlk_value)

    return temp_data_dict


def PUT_query(data,trie_server_dict):
    data_dict = json_to_dict(data)

    # nested trie
    tr.nested_trie(trie_server_dict, data_dict) 
    
    return 9


def DELETE_query(key,trie_server_dict):
    key = re.sub("[\"']", "", key)
    success = tr.trie_delete_key(trie_server_dict, key)
    if success==9:
        response="OK"
    else:
        response="NO"
    return response


def GET_query(data,trie_server_dict):
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
    key_path = data.split(".")
    for i,k in enumerate(key_path):
        key_path[i] = key_path[i].rstrip(" ")
        key_path[i] = key_path[i].lstrip(" ")
    
    key = key_path[0]
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, key_path)

    if found:
        response = f"{'.'.join(key_path)} : {val_dict}"
    else:
        response=" "
    return response