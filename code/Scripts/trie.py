#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

class Trie_Node():
    '''
    Trie structure node for key storing
    '''

    def __init__(self,character):
        self.character = character
        
        # previous and next characters of the current
        self.parent_node = None
        self.children_nodes = [ ]
        
        # if node indicates end of key(word) and the respective key(whole string)
        self.end_of_word = False
        self.key = None
        
        # if end_of_word==True, this indicates a key with the following nested keys and value
        self.nested_keys = []
        # value can be a set(empty/non-empty), string, float, int 
        self.value = None

        # if top - level key
        self.istop_level_key = False

        # nested trie with the nested keys/values
        self.nested_trie = None

    def __del__(self):
        self.character = None
        self.parent_node = None
        self.children_nodes = [ ]
        self.end_of_word = False
        self.key = None
        self.nested_keys = []
        self.value = None
        self.istop_level_key = False
        self.nested_trie = None


def insert_child(children_list,new_child):
    ''' 
    Sorted insertion of new character (node child) in the previous character's children node list
    '''

    if len(children_list)==0:
        children_list.append(new_child)
        return children_list  

    pos = 0
    for position, child in enumerate(children_list):
        while new_child.character > child.character:
            pos+=1
            break
    
    children_list.insert(pos,new_child)
    return children_list  
      

def trie_insert_key(trie_dictionary, key, value, istop_level_key):
    ''' 
    Insertion of new word (key) in a trie dictionary.
    For each character of the new key, the function searches the "trie_dictionary" structure. If part of it is found then the rest of the key-word is inserted after the prefix found
    '''
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
            curr_node = new_child
            
    # Setting the last node of the key-word  as end of word, indicating a key (either top-level or not)
    curr_node.end_of_word = True
    curr_node.istop_level_key = istop_level_key
    curr_node.key = key

    return curr_node


def insert_nested_trie(node, data_dict):
    ''' 
    Inserts the nested keys/values in the nested trie structures of the respective top level key.
    The function recursively traverses all the nesting levels (all key-value pairs at each level) of the value dictionary of the top-level key and stores the value of each nested key at the nested trie structure of the top level key word's last node (if the value is a dictionary with nested key-value pairs, the value is "None", the default value of a trie node)
    '''

    curr_node = node
    if type(data_dict)!=type(dict()) or data_dict=={}:
        node.value = data_dict
        return -1
    
    curr_node.nested_trie = Trie_Node(".")
    for k in data_dict.keys():
        curr_node.nested_keys.append(k)
        node = trie_insert_key(curr_node.nested_trie, k, value=None, istop_level_key=False)
        insert_nested_trie(node, data_dict[k])
    
    return -1


def nested_trie(trie_dict, data_dict):
    '''
    Inserts new entry by storing its top-level key in the main trie first and then the nested keys/values in the respective nested trie structures. If the top level key is found, it is discarded
    '''

    tl_key = list(data_dict.keys())[0]
    found,val,node = trie_find_key(trie_dict, tl_key)
    if found:
        return -9
    else:
        node = trie_insert_key(trie_dict, tl_key, value=None, istop_level_key=True)
        insert_nested_trie(node,data_dict[tl_key])
    
    return 9


def trie_get_value_nested(node):
    '''
    Gets the value of a keypath, either a single value (int, float, string), empty set ({}) or dictionary with nested key-value pairs by recursively traversing the nesting levels and the nested keys of each level of the node's nested trie (value dictionary) 
    '''

    if node.value != None or node.value=={}:
        return node.value

    val_dict = {}
    k_nested = node.nested_trie
    for key in node.nested_keys:
        found,value,new_node = trie_find_key(k_nested, key)
        val_dict[key] = trie_get_value_nested(new_node)

    return val_dict


def trie_find_keypath_nested(trie_dict,keypath_list):
    '''
    If the top level key exists, the function returns the value of that key. If the keypath (keypath_list) includes other nested keys, it searches for the last node of the keypath (last key's node) and returns the respective value using the function "trie_get_value_nested" above 
    '''
    
    found,val,tl_key_node = trie_find_key(trie_dict, keypath_list[0])
    if tl_key_node==None:
        return False,None
    if len(keypath_list)==1:
        val_dict = trie_get_value_nested(tl_key_node)
        return val_dict!=None,val_dict
    elif len(keypath_list)>1:
        node = tl_key_node
        for key in keypath_list[1:]:
            if key in node.nested_keys:
                found,val,node = trie_find_key(node.nested_trie, key)
                if node==None:
                    return False,None
            else:
                return False,None

    val_dict = trie_get_value_nested(node)
    
    return val_dict!=None,val_dict


def trie_find_key(trie_dictionary,key):
    '''
    Searches for a certain key in the given trie structure and returns if it is found, its value and the node of the last character
    '''

    word_found = False
    curr_node = trie_dictionary
    value = None
    node_found = None

    for letter in key:
        letter_found = False
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                curr_node=child_node
                letter_found = True
                break
            
        if letter_found == False:
            return word_found,value,None

    if letter_found == True and curr_node.end_of_word == True:
        word_found = True
        value = curr_node.value
        node_found = curr_node

    return word_found, value, node_found


def trie_delete_key(trie_dictionary,key):
    '''
    Deletes the top level key of an entry.
    If the key is found, after reaching the last node of the key-word, the function "deletes" each character node by following the parent node of each, till it finds a prefix used by another key word where it stops
    '''

    found_flag, value, key_node = trie_find_key(trie_dictionary,key)
    if found_flag==True:
        # This ensures that if the key we want to delete is inside a used prefix, it does not indicate a key (end of word) anymore
        key_node.end_of_word = False
        key_node.istop_level_key = False
        key_node.nested_keys = []
        key_node.key = None
        key_node.nested_trie = None
        key_node.value = None

        temp_node = key_node
        while temp_node!=None:
            curr_node = temp_node
            temp_node = temp_node.parent_node
            if len(curr_node.children_nodes)==0:
                parent = temp_node
                if temp_node!=None and curr_node in temp_node.children_nodes:
                    temp_node.children_nodes.remove(curr_node)
                
                del curr_node

        found_flag, value, key_node = trie_find_key(trie_dictionary,key)
            
    else:
        return -9

    return 9


def delete_trie(trie_server_dict):
    '''
    Deletes the root node of the server's trie database
    '''

    del trie_server_dict

