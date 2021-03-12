import trie as tr

data_filepath = "../data/"

# temp_list = ["theatina", "doyouevenexist", "no", "piano"]

temp = ["bear", "bell", "bid", "bull", "buy", "sell", "stock", "stop"]

trie_dictionary = tr.trie_node(".")

# for word in temp:
    # trie_dictionary.insert(word)

trie_dictionary.insert("bear")
print(trie_dictionary.find_word("bear"))

# trie_dictionary.print_trie()