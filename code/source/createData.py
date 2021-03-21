#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
 
Christina-Theano Kylafi
M111 - Big Data
LT1200012

'''

import os
import createData_funs as cdf

data_filepath = "../data/"
keyfile_path = os.path.join(data_filepath,"keyFile.txt")
dataToIndex_path =  os.path.join(data_filepath,"dataToIndex.txt")
namesTextFile_path =  os.path.join(data_filepath,"nameFile.txt")

keyfile_path,file_lines = cdf.arg_parsing(keyfile_path)
cdf.key_dictionaries(keyfile_path)

# create data file
data2index = open(dataToIndex_path,"w+",encoding="utf-8")
cdf.save_names(namesTextFile_path)

for line in range(file_lines):
    row_data = cdf.data_row_creation(line)
    data2index.write(row_data)

data2index.close()
exit()