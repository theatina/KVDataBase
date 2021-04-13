#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import re 
import argparse
import itertools
import random
import time
from datetime import datetime
import numpy as np
import string
import os
import customExceptions as ce

def input_check(args):
    '''
    Performs input checks concerning the keyFile.txt, the number of lines, the nesting levels, the number of keys at each level and the maximum string length for the values of type "string" and raises an exception in case of error
    '''

    try:
        if not os.path.exists(args.k):
            raise ce.UsrInputError(f"\nERROR: File '{args.k}' does not exist!!\n") 
        if args.n < 1:
            raise ce.UsrInputError(f"\nERROR: Lines must be > 0 ( '{args.n}' value was given )\n")
        if args.d < 0:
            raise ce.UsrInputError(f"\nERROR: Max nesting level must be > 0 ( '{args.d}' value was given )\n")
        if args.m < 1:
            raise ce.UsrInputError(f"\nERROR: Max number of keys must be > 0 ( '{args.m}' value was given )\n")
        if args.l < 1:
            raise ce.UsrInputError(f"\nERROR: Max string length must be > 0 ( '{args.l}' value was given )\n")


        # Here, a check is performed to ensure that the unique keys in the keyFile.txt are not less than the number of keys in each nesting level, because no duplicates are allowed, so errors will occur
        with open(args.k,"r",encoding="utf-8") as reader:
            unique_keys = len(reader.read().strip().split("\n"))
        
        if args.m > unique_keys:
            raise ce.UsrInputError(f"\nERROR: Max number of keys/level must be <= unique keys in '{args.k}' ( '{args.m}' value was given > {unique_keys} unique keys in file )\n")

        if args.d > 1000:
            raise ce.UsrInputError(f"\nERROR: Max nesting level must be <= 1000 ( '{args.d}' value was given )\n")

    except ce.UsrInputError as err:
        print(err.args[0])
        exit()


max_nesting,max_keys_each_level,max_str_len=0,0,0
def arg_parsing(keyfile_path):
    '''
    Command line input parser/checker.
    Global variables max_nesting, max_keys_each_level and max_str_len are also updated in this function in order to be used for the data creation later
    '''
    # Command: createData -k keyFile.txt -n 10 -d 3 -l 4 -m 9
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=str, default=keyfile_path, help=" Key list textfile ")
    parser.add_argument("-n", type=int, default=10, help=" Number of lines ")
    parser.add_argument("-d", type=int, default=3, help=" Maximum level of nesting ")
    parser.add_argument("-m", type=int, default=4, help=" Maximum number of keys / each value ")
    parser.add_argument("-l", type=int, default=9, help=" Maximum length of string value ")
    
    args = parser.parse_args()
    input_check(args)

    global max_nesting,max_keys_each_level,max_str_len
    max_nesting,max_keys_each_level,max_str_len = args.d, args.m, args.l

    return args.k,args.n


key_type_dict,all_key_types_dict = {},{}
def key_dictionaries(keyfile_path):
    '''
    This function creates 2 dictionaries from the keyFile.txt: 
    1 that contains key:value_type pairs (e.g. 'name': 'string') and
    1 that contains value_type:[key_names] entries (e.g. 'string': ['name', 'profession'])
    for later use in the process of data creation
    '''
    
    global key_type_dict,all_key_types_dict
    
    key_file = open(keyfile_path,"r",encoding="utf-8").read().strip().split("\n")
    
    key_n_type = [ tuple(k.split(" ")) for k in key_file if len(k.split(" "))==2 ]
    key_n_type = sorted(key_n_type, key = lambda y:y[1])
    key_type_dict = {kt[0]:kt[1] for kt in key_n_type }
    group_fun = lambda f: f[1]   
    for key, group in itertools.groupby(key_n_type, group_fun): 
        all_key_types_dict[key] = [ pair[0] for pair in list(group) ]


def level_keys(): 
    '''
    At each nesting level, the function first picks a random number (keys_num) indicating the number of keys at that level ( <= max_keys_each_level ) and then chooses a sample of keys_num numbers, representing the indices of the unique keys from keyFile.txt
    '''

    # Use of time seed to not have the same numbers at each function execution
    random.seed(datetime.now())
    max_key_index = len(key_type_dict)
    # 10% probability of an empty set ( {} ) as value
    non_empty = random.randint(0, 9)
    key_list = []
    if non_empty:
        keys_num = random.randint(1, max_keys_each_level)
        keys = random.sample(range(0, max_key_index), keys_num)

        key_list = [ key for i,key in enumerate(key_type_dict.keys()) if i in keys ]

    return key_list


global name_list
def save_names(filepath):
    '''
    Loads nameFile.txt and saves a list with potential names to be used as "name" key values
    '''

    global name_list
    name_list = open(filepath,"r",encoding="utf-8").read().split("\n")


def rand_str_generator():
    ''' 
    Random string generator for keys with 'string' value type.
    Creates strings with upper/lowercase ascii letters and digits of length 'word_len' ( <=max_str_len )
    '''

    word_len = random.randint(1,max_str_len)
    r_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(word_len))

    return r_str


def create_value(key):
    ''' 
    Creates a value of string, int or float for the given key. If the key name is "name" then the value is randomly choosen from a list of names saved before (name_list)
    '''

    val = {}
    random.seed(datetime.now())
    
    # 20% probability of an empty set ( {} ) as value
    non_empty_val = random.randint(0, 4)
    if non_empty_val:
        get_key_type = key_type_dict[key]

        if get_key_type == "int":
            val = random.randint(1,200)
        elif get_key_type == "float":
            upper_bound = random.randint(1,100)
            val = random.uniform(0.0, float(upper_bound))
            val = round(val,2)
        elif get_key_type == "string":
            if "name" in key:
                name_id = random.randint(0,len(name_list)-1)
                val = name_list[name_id]
            else:
                val = rand_str_generator()

    return val


global key_nesting
def value_level(keys,depth):
    ''' 
    Recursive function that creates a value dictionary for each top level key, by creating the value/value dictionary of each of the nested keys recursively.
    At each execution for each key, the depth increases and the key_nesting takes random values between 0 and max_nesting-(depth+1) until it takes a value of zero ( (depth+1) == max_nesting ), where the value of those keys has to be either a string, float, int or empty set and not a set of key-value pairs, so it stops the recursion process
    '''

    global key_nesting

    temp_d = {}
    for key in keys:

        if key_nesting==0:
            temp_d[key] = create_value(key)
        else: 
            depth+=1
            key_nesting = random.randint(0,max_nesting-depth)
            # Nested key list
            keys = level_keys()
            # Value for each key
            temp_d[key]=value_level(keys,depth)

    return temp_d


def textfile_modifications(data,value):
    ''' 
    Entry modifications to result in the desired format described in the instructions
    '''

    data+=str(value)+"\n"
    data = re.sub(r","," ;", data)
    data = re.sub(r"'","\"", data)
    data = re.sub(r"\":","\" :", data)
    data = re.sub(r"{\"","{ \"", data)
    data = re.sub(r"}"," }", data)
    data = re.sub(r"{ }","{}", data)

    return data


def data_row_creation(line_num):
    ''' 
    For each row, a top level key is created and then a value dictionary is formed by using the recursive function "value_level()" for the multiple nestings
    '''

    global key_nesting

    value = {}
    top_level_key = "tlkey"
    data_row = "\""+top_level_key+str(line_num+1)+"\" : "  

    level_0_keys = level_keys()
    # depth starts with 0 value (top level key value)
    depth=0
    # nesting starts with max_nesting
    key_nesting=max_nesting
    # The nesting level starts 
    value = value_level(level_0_keys,depth)
    
    data_row = textfile_modifications(data_row,value)

    return data_row


def create_entry_file(file_lines,dataToIndex_path,namesTextFile_path):
    ''' 
    A file is created, with file_lines number of entries.
    Each entry is created by using the data_row_creation() function above
    '''
    
    save_names(namesTextFile_path)
    data2index = open(dataToIndex_path,"w+",encoding="utf-8")
    for line in range(file_lines):
        row_data = data_row_creation(line)
        data2index.write(row_data)
    
    data2index.close()
