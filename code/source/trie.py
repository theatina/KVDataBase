#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
 
Christina-Theano Kylafi
M111 - Big Data
LT1200012

'''

# trie structure node module

# class value_node():
    
#     def __init__(self, value):
#         self.value = value
#         self.nesting_level = -1
#         self.next_level = None
#         self.prev_level = None

class trie_node():

    def __init__(self,character):
        self.character = character
        self.parent_node = None
        self.children_nodes = [ ]
        
        self.end_of_word = False
        
        # if end_of_word==True, this indicates a key with the following value or nested keys
        self.nested_keys = []
        self.value = None
        self.type = None

        # if top/high - level key
        self.top_level_key = False
        
    
def insert_child(children_list,new_child):

    if len(children_list)==0:
        children_list.append(new_child)
        return children_list  

    pos = 0
    for position, child in enumerate(children_list):
        while new_child.character > child.character:
            # print(position,child.character,new_child.character)
            pos+=1
            break
    
    # print(new_child.character,pos)
    children_list.insert(pos,new_child)
    return children_list  
      

# insertion of word in the trie dictionary
def trie_insert_key(trie_dictionary, key, value, top_level_key):
    curr_node = trie_dictionary
    for letter in key:
        char_in_trie = False
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                char_in_trie = True
                curr_node = child_node
                break
        
        if char_in_trie == False:
            new_child = trie_node(letter)
            new_child.parent_node = curr_node
            
            curr_node.children_nodes = insert_child(curr_node.children_nodes,new_child)
            # curr_node.children_nodes.append(new_child) 
        
            curr_node = new_child
            
    curr_node.end_of_word = True
    

def trie_find_key(trie_dictionary,key):
    word_found = False
    curr_node = trie_dictionary
    value = None

    for letter in key:
        letter_found = False
        # children_chars = [i.character for i in curr_node.children_nodes ]
        # print(f"{children_chars}")
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                curr_node=child_node
                letter_found = True
                break
            
        if letter_found == False:
            return word_found,value

    if letter_found == True and curr_node.end_of_word == True:
        word_found = True
        value = curr_node.value
    
    return word_found, value


def trie_print_words(trie_dictionary):
    temp_word = ""
    end_of_word = False
    trie_node = trie_dictionary

    # while end_of_word==0:
        

    # def delete_trie(self):
