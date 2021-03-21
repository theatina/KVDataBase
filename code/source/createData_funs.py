import re 
import argparse
import itertools
import random
import time
from datetime import datetime
import numpy as np
import string
import os

class UsrInputError(Exception):
    pass

def input_check(args):
    
    try:
        if not os.path.exists(args.k):
            raise UsrInputError(f"\nERROR: Path '{args.k}' does not exist!!\n") 
        if args.n < 1:
            raise UsrInputError(f"\nERROR: Lines must be > 0 ( '{args.n}' value was given )\n")
        if args.d < 0:
            raise UsrInputError(f"\nERROR: Max nesting level must be > 0 ( '{args.d}' value was given )\n")
        if args.m < 1:
            raise UsrInputError(f"\nERROR: Max number of keys must be > 0 ( '{args.m}' value was given )\n")
        if args.l < 1:
            raise UsrInputError(f"\nERROR: Max string length must be > 0 ( '{args.l}' value was given )\n")

    except UsrInputError as err:
        print(err.args[0])
        exit()


max_nesting,max_keys_each_level,max_str_len=0,0,0
def arg_parsing(keyfile_path):
    # Command: createData -k keyFile.txt -n 1000 -d 3 -l 4 -m 5
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=str, default=keyfile_path, help=" Key list textfile ")
    parser.add_argument("-n", type=int, default=10, help=" Number of lines ")
    parser.add_argument("-d", type=int, default=9, help=" Maximum level of nesting ")
    parser.add_argument("-m", type=int, default=3, help=" Maximum number of keys / each value ")
    parser.add_argument("-l", type=int, default=8, help=" Maximum length of string value ")
    args = parser.parse_args()
    input_check(args)
    # print(args)
    global max_nesting,max_keys_each_level,max_str_len
    max_nesting,max_keys_each_level,max_str_len = args.d, args.m, args.l

    return args.k,args.n#,args.d,args.m,args.l


key_type_dict,all_key_types_dict = {},{}
def key_dictionaries(keyfile_path):
    global key_type_dict,all_key_types_dict

    key_n_type = [ tuple(k.split(" ")) for k in open(keyfile_path,"r",encoding="utf-8").read().split("\n") ]
    key_n_type = sorted(key_n_type, key = lambda y:y[1])
    key_type_dict = {kt[0]:kt[1] for kt in key_n_type }
    # all_key_types_dict = {}
    group_fun = lambda f: f[1]   
    for key, group in itertools.groupby(key_n_type, group_fun): 
        all_key_types_dict[key] = [ pair[0] for pair in list(group) ]


    # return key_type_dict,all_key_types_dict


def level_keys(): 
    # global key_type_dict,all_key_types_dict
    random.seed(datetime.now())
    max_key_index = len(key_type_dict)
    # print(key_type_dict, max_key_index, max_keys_each_level)
    keys_num = random.randint(1, max_keys_each_level+1)
    keys = random.sample(range(0, max_key_index), keys_num)
    # key_list(np.random.randint(low = 3,high=8,size=10)))
    key_list = [ key for i,key in enumerate(key_type_dict.keys()) if i in keys ]
    print(keys_num, key_list) 
    return key_list

global name_list
def save_names(filepath):
    global name_list
    name_list = open(filepath,"r",encoding="utf-8").read().split("\n")
    # print(name_list)

def rand_str_generator():
    word_len = random.randint(1,max_str_len)
    r_str = ''.join(random.choices(string.ascii_lowercase, k = word_len)) 
    print(r_str)
    return r_str

def create_value(key):
    val = {}
    random.seed(datetime.now())
    non_empty_val = random.randint(0, 1)
    print(f"empty val: {non_empty_val}")
    if non_empty_val:
        get_key_type = key_type_dict[key]
        print(get_key_type)
        if get_key_type == "int":
            val = random.randint(1,200)
        elif get_key_type == "float":
            val = random.random()
            val = round(val,2)
        elif get_key_type == "string":
            if "name" in key:
                name_id = random.randint(0,len(name_list))
                val = name_list[name_id]
            else:
                val = rand_str_generator()

    return val


global key_nesting
def value_level(keys,level):
    global key_nesting

    temp_d = {}
    for key in keys:
        if key_nesting==0:
            temp_d[key] = create_value(key)
        else: 
            key_nesting = random.randint(0,max_nesting-level)
            keys = level_keys()
            # print(f"nesting: {key_nesting}")
            temp_d[key]=value_level(keys,level+1)

    return temp_d


def data_row_creation(line_num):
    global level_max_nesting
    global key_nesting

    value = {}
    top_level_key = "key"
    data_row = "\""+top_level_key+str(line_num+1)+"\" : "#+str(value)+"\n"  

    level_0_keys = level_keys()
    # for i,key in enumerate(level_0_keys):
    # level_0_key_nesting = random.randint(0,max_nesting)
    level_max_nesting = max_nesting
    depth=0
    key_nesting=max_nesting
    value = value_level(level_0_keys,depth)
    print(value)
    # value[key]=temp_value
     
    data_row+=str(value)+"\n"
    data_row = re.sub(","," ;", data_row)
    
    return data_row