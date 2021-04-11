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

class Trie_Node():

    def __init__(self,character):
        self.character = character
        self.parent_node = None
        self.children_nodes = [ ]
        
        self.end_of_word = False
        self.key = None
        
        # if end_of_word==True, this indicates a key with the following value or nested keys
        self.nested_keys = []
        # value can be a set(empty/non-empty), string, float, int 
        self.value = None
        self.value_list = []
        self.value_type = type(self.value)
        # dictionary with all the keypaths and their respective values
        self.keypath_list = []

        # if top/high - level key
        self.istop_level_key = False

        # nested trie
        self.nested_trie = None


    def __del__(self):
        self.character = None
        self.parent_node = None
        self.children_nodes = [ ]
        self.end_of_word = False
        self.key = None
        self.nested_keys = []
        self.value = None
        self.value_type = None
        self.keypath_list = []
        self.istop_level_key = False
        self.nested_trie = None


def insert_value(trie_insert_key,new_child,value):
    new_child.value_list.append(value)

    return new_child
    

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
def trie_insert_key(trie_dictionary, key, value, istop_level_key):
    curr_node = trie_dictionary
    for letter in key:
        char_in_trie = False
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                char_in_trie = True
                curr_node = child_node
                break
        
        if char_in_trie == False:
            new_child = Trie_Node(letter)
            new_child.parent_node = curr_node
            
            curr_node.children_nodes = insert_child(curr_node.children_nodes,new_child)
            # curr_node.children_nodes.append(new_child) 
        
            curr_node = new_child
            
    curr_node.end_of_word = True
    curr_node.istop_level_key = istop_level_key
    curr_node.key = key
    insert_value(trie_dictionary,curr_node,value)
    return curr_node

def trie_insert_keypaths(trie_dictionary, key, keypath, istop_level_key, value, nested_key_list):
    curr_node = trie_dictionary
    for letter in key:
        char_in_trie = False
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                char_in_trie = True
                curr_node = child_node
                break
        
        if char_in_trie == False:
            new_child = Trie_Node(letter)
            new_child.parent_node = curr_node
            
            curr_node.children_nodes = insert_child(curr_node.children_nodes,new_child)
            # curr_node.children_nodes.append(new_child) 
        
            curr_node = new_child
            
    curr_node.end_of_word = True
    curr_node.istop_level_key = istop_level_key
    if curr_node.key==None:
        curr_node.key = key
    curr_node.keypath_list.append(keypath)
    curr_node.nested_keys.append(nested_key_list)
    insert_value(trie_dictionary,curr_node,value)

kpath = []
def trie_insert_entry(trie_dictionary, entry_data_dictionary, keypath):
    global kpath
    # print(entry_data_dictionary)
    istop_level_key=False
    value = None

    if type(entry_data_dictionary)!=type(dict()):
        # print(f"type:{type(entry_data_dictionary)}")
        return entry_data_dictionary
    
    for i,key in enumerate(entry_data_dictionary.keys()):
        temp_keypath = keypath.copy()
        temp_keypath.append(key)
        # print(temp_keypath,key)
        
        value = trie_insert_entry(trie_dictionary,entry_data_dictionary[key],temp_keypath)
        if len(temp_keypath)==1:
            istop_level_key=True
        
        nested_key_list=[]
        if type(entry_data_dictionary[key])==type(dict()):
            # print(key,list(entry_data_dictionary[key].keys()))
            nested_key_list = list(entry_data_dictionary[key].keys())

        trie_insert_keypaths(trie_dictionary, key, temp_keypath, istop_level_key, value, nested_key_list)
        istop_level_key=False

    return None


def insert_nested_trie(node, data_dict):
    curr_node = node
    # print(f"'{data_dict}'")
    if type(data_dict)!=type(dict()) or data_dict=={}:
        # print(data_dict)
        node.value = data_dict
        return -1
    
    curr_node.nested_trie = Trie_Node(".")
    for k in data_dict.keys():
        curr_node.nested_keys.append(k)
        node = trie_insert_key(curr_node.nested_trie, k, value=None, istop_level_key=False)
        insert_nested_trie(node, data_dict[k])

    return -1


def nested_trie(trie_dict, data_dict):

    tl_key = list(data_dict.keys())[0]
    node = trie_insert_key(trie_dict, tl_key, value=None, istop_level_key=True)
    # print(node.key)
    insert_nested_trie(node,data_dict[tl_key])
    # print(node.nested_trie.children_nodes)
    # print(node.nested_keys)
    # print(trie_get_value_nested(node))
    # print(trie_find_keypath_nested(trie_dict,["tl_key1","street"]))
    
    pass

    
def data_indexing_from_file(trie_dict,filepath):
    lines = open(filepath,"r",encoding="utf-8").read().split("\n")

def trie_get_value_nested(node):
    if node.value != None and node.value!={}:
        return node.value 

    # found = False
    # new_node = None
    # value = None
    val_dict = {}
    # print(node.nested_trie.children_nodes,node.nested_keys)
    k_nested = node.nested_trie
    for key in node.nested_keys:
        found,value,new_node = trie_find_key(k_nested, key)
        # print(key,new_node,value)
        val_dict[key] = trie_get_value_nested(new_node)
        # print(key)

    return val_dict

def trie_find_keypath_nested(trie_dict,keypath_list):
    found,val,tl_key_node = trie_find_key(trie_dict, keypath_list[0])
    if tl_key_node==None:
        return False,{}
    if len(keypath_list)==1:
        val_dict = trie_get_value_nested(tl_key_node)
        return val_dict!={},val_dict
    elif len(keypath_list)>1:
        node = tl_key_node
        for key in keypath_list[1:]:
            if key in node.nested_keys:
                found,val,node = trie_find_key(node.nested_trie, key)
                if node==None:
                    return False,{}
            else:
                return False,{}
    # print(node.key)
    val_dict = trie_get_value_nested(node)
    return val_dict!={},val_dict

def trie_find_tl_key_nested(trie_dict,keypath_list):
    found,val,tl_key_node = trie_find_key(trie_dict, keypath_list[0])
    if tl_key_node==None:
        return False,{}
    val_dict = trie_get_value_nested(tl_key_node)
    return val_dict!={},val_dict

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
                # print(letter,child_node.character)
                curr_node=child_node
                letter_found = True
                break
            
        if letter_found == False:
            return word_found,value,None

    if letter_found == True and curr_node.end_of_word == True:
        word_found = True
        value = curr_node.value
    
    return word_found, value, curr_node


def trie_delete_key(trie_dictionary,key):

    found_flag, value, key_node = trie_find_key(trie_dictionary,key)
    if found_flag==True:
        key_node.end_of_word = False
        key_node.istop_level_key = False
        key_node.nested_keys = []
        key_node.key = None
        key_node.nested_trie = None

        temp_node = key_node
        while temp_node!=None:
            curr_node = temp_node
            temp_node = temp_node.parent_node
            if len(curr_node.children_nodes)==0:
                parent = temp_node
                if temp_node!=None and curr_node in temp_node.children_nodes:
                    temp_node.children_nodes.remove(curr_node)
                
                del curr_node

    
            # elif:
        found_flag, value, key_node = trie_find_key(trie_dictionary,key)
        # print(found_flag)     
            
    else:
        # print(f"\nKey '{key}' was not found! ( DELETE failed )\n")
        return -9

    return 9


# def trie_delete_key_nested(trie_dictionary,key):
#     found_flag, value, key_node = trie_find_key(trie_dictionary,key)
#     node = key_node
#     nested_keys_trie = []
#     if found_flag==True:
#         while node.nested_trie:

#             nested_keys_trie.append()
        
        
#         # the final node - top level key
#         trie_delete_key(trie_dictionary,key)

#     else:
#         # print(f"\nKey '{key}' was not found! ( DELETE failed )\n")
#         return -9
    
#     return 9


def delete_trie(trie_server_dict):
    # for top_level_key in trie_server_dict.children_list:
    #     while node.istop_level_key==False:
    #         # node = 
        
    #     trie_delete_key_nested()
    del trie_server_dict
    
    pass

# def trie_print_words(trie_dictionary):
#     temp_word = ""
#     end_of_word = False
#     trie_node = trie_dictionary

    # while end_of_word==0:
        

    # def delete_trie(self):
