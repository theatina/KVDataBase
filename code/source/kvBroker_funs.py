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
        if not os.path.exists(args.s):
            raise UsrInputError(f"\nERROR: File '{args.s}' does not exist!!\n") 
        if not os.path.exists(args.i):
            raise UsrInputError(f"\nERROR: File '{args.i}' does not exist!!\n") 
        if args.k < 1:
            raise UsrInputError(f"\nERROR: Server number must be > 0 ( '{args.k}' value was given )\n")

    except UsrInputError as err:
        print(err.args[0])
        exit()


def arg_parsing(serverFile_path,dataToIndex_path):
    
    # Command: kvBroker -s serverFile.txt -i dataToIndex.txt -k 2    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default=serverFile_path, help=" Server ip-port list ")
    parser.add_argument("-i", type=str, default=dataToIndex_path, help=" Data ")
    parser.add_argument("-k", type=int, default=9, help=" Pick random k servers ")
    args = parser.parse_args()
    input_check(args)

    return args.s,args.i,args.k


def read_file(filepath):
    return open(filepath,"r",encoding="utf-8").read().split("\n")