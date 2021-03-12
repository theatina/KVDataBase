class trie_node():

    def __init__(self,character):
        self.character = character
        self.parent_node = None
        self.children_nodes = [ ]
        self.end_of_word = False
        
    
    # insertion of word in the trie structure
def insert(self, word):
    curr_node = self
    for letter in word:
        char_in_trie = False
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                char_in_trie = True
                curr_node = child_node
                break
        
        if char_in_trie == False:
            new_child = trie_node(letter)
            curr_node.children_nodes.append(new_child)   
            curr_node = curr_node.children_nodes[-1]
            
    curr_node.end_of_word = True
    
    print(self.children_nodes)

def find_word(self,word):
    word_found = False
    curr_node = self
    
    for letter in curr_node.children_nodes:
        letter_found = False
        
        for child_node in curr_node.children_nodes:
            if letter == child_node.character:
                print(letter)
                curr_node=child_node
                letter_found = True
                break
            
        if letter_found == False:
            return word_found

    if letter_found == True and curr_node.end_of_word == True:
        word_found = True
    
    return word_found


def print_words(self):
    temp_word = ""
    end_of_word = False
    trie_node = self

    # while end_of_word==0:
        

    # def delete_trie(self):
