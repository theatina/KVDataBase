#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Christina-Theano Kylafi
M111 - Big Data
LT1200012
'''

import os
import createData_funs as cdf

print(f"\nCreating Data..\n")
data_filepath = "../data/"
keyfile_path = os.path.join(data_filepath,"keyFile.txt")
dataToIndex_path =  os.path.join(data_filepath,"dataToIndex.txt")
namesTextFile_path =  os.path.join(data_filepath,"nameFile.txt")

# Input checks
keyfile_path,file_lines = cdf.arg_parsing(keyfile_path)
cdf.key_dictionaries(keyfile_path)

# Creates the entry data file
cdf.create_entry_file(file_lines,dataToIndex_path,namesTextFile_path)

exit()