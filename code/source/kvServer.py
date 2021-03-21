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

data_filepath = "../data/"

# Command: kvServer -a ip_address -p port
parser = argparse.ArgumentParser()
parser.add_argument("-a", type=str, default=" ")
parser.add_argument("-p", type=int, default=" ")
args = parser.parse_args()

print(args)






'''
# temp_list = ["theatina", "doyouevenexist", "no", "piano"]

temp = ["abchsdf", "lalal", "sham", "shame", "wax", "bear", "bell", "bid", "bull", "buy", "sell", "stock", "stop", "theatina"]

trie_dictionary = tr.Trie_Node(".")

value = None
top_level_key = False
for word in temp:
    tr.trie_insert_key(trie_dictionary,word,value,top_level_key)

for i,word in enumerate(temp):
    if_found,sth = tr.trie_find_key(trie_dictionary,word)
    if if_found == True :
        found = "Found"
    else:
        found = "Not found"

    print(f"{i}. {word}: {found}")

# trie_dictionary.print_trie()

'''