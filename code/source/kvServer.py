#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
 
Christina-Theano Kylafi
M111 - Big Data
LT1200012

'''

import trie as tr
import argparse

data_filepath = "../data/"

# Command: kvServer -a ip_address -p port


# The programme can be run as " python ./final_project_test --source <dataset_source_folder_path> " or as " python ./final_project_test ", where the default path of the dataset folder is " ./test_data_901_final_project/ "
parser = argparse.ArgumentParser()
parser.add_argument("-a", type=str, default=" ")
parser.add_argument("-p", type=int, default=" ")
args = parser.parse_args()

print(args)






'''
# temp_list = ["theatina", "doyouevenexist", "no", "piano"]

temp = ["bear", "bell", "bid", "bull", "buy", "sell", "stock", "stop", "9", "theatina"]

trie_dictionary = tr.trie_node(".")

value = None
top_level_key = False
for word in temp:
    tr.trie_insert_key(trie_dictionary,word,value,top_level_key)

for i,word in enumerate(temp):
    if tr.trie_find_key(trie_dictionary,word) == True:
        found = "Found"
    else:
        found = "Not found"

    print(f"{i}. {word}: {found}")

# trie_dictionary.print_trie()

'''