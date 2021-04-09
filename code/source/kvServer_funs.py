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


def CHECK_query(data,trie_server_dict):
    # print(f"\nServer Check\n")
    # print(f"Data: {data}")
    pass

def json_to_dict(data):
    temp_data_dict = {}
    if data!="{}":
        if ";" in data:
            data = re.sub(";", ",", data)
        
        top_level_key,tlk_value = data.split(" : ", maxsplit=1)
        top_level_key = top_level_key.strip("\"")
        # print(f"Jason:{tlk_value}")
        temp_data_dict[top_level_key] = json.loads(tlk_value)

    return temp_data_dict

def PUT_query(data,trie_server_dict):
    # global keypath
    
    # print(f"\nPUT request\n")
    data_dict = json_to_dict(data)
    # print(print(f"Data: {data_dict}"))
    
    # nested trie
    tr.nested_trie(trie_server_dict, data_dict) 

    # keypath = []
    # tr.trie_insert_entry(trie_server_dict, data_dict, keypath)
    # for k in data_dict.keys():
    #     found,val,key_node = tr.trie_find_key(trie_server_dict, k)
    #     print(f"key: {key_node.key} keypath dict: {key_node.keypath_list}")

    # test_key = "postal_code"
    # found,val,key_node = tr.trie_find_key(trie_server_dict, test_key)
    # if found:
    #     print(f"\nkey: {key_node.key} keypath dict: {key_node.keypath_list}")
    
    pass


def GET_query(data,trie_server_dict):
    # print(f"\nGET request\n")
    # print(f"Data: {data}")
    key_path = data.split(".")
    key = key_path[0]
    val_dict = {}
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, key_path)
    # GET key
    # searches the nested keys and the keypaths(if the top level key is the desired) to create the data row

    # Get keypath
    # searches for the last key of the path and its respective keypath dictionary to get the value of the certain keypath if it exists
    # val = {}
    # val[key] = val_dict
    if found:
        response = f"{key} : {val_dict}"
    else:
        response=" "
    return response

def DELETE_query(key,trie_server_dict):
    # print(f"\nDELETE request\n")
    # print(f"Data: {key}")
    success = tr.trie_delete_key_nested(trie_server_dict, key)
    return success

def QUERY_query(data,trie_server_dict):
    # print(f"\nQUERY request\n")
    # print(f"Data: {data}")
    key_path = data.split(".")
    key = key_path[0]
    # print(key)

    # test_key = "postal_code"
    # found,val,key_node = tr.trie_find_key(trie_server_dict, key)
    found,val_dict = tr.trie_find_keypath_nested(trie_server_dict, key_path)
    # print(trie_server_dict)
    # if found:
    #     print(f"\n{data}: {val_dict}")
    #     # print(f"\nKey: {key_node.key} \nKeypaths: {key_node.keypath_list}\nValue: {key_node.value_list}")
    #     # for i,path in enumerate(key_node.keypath_list):
    #     #     print((path,key_path,key_node.istop_level_key))
    #     #     if key_path==path:
    #     #         print(f"\nKey: '{key_node.key}' \nKeypath: {path}\nValue: {key_node.value_list[i]}\nTop_level_key: {key_node.istop_level_key}\nNested_keys: {key_node.nested_keys[i]}")
    #     #         break
    # else:
    #     if len(key_path)==1:
    #         print(f"\nKey '{data}' not found!")
    #     else:
    #         print(f"\nKeypath '{data}' not found!")
    if found:
        response = f"{data} : {val_dict}"
    else:
        response=" "
    return response