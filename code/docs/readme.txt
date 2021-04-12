Christina-Theano Kylafi
M111 - Big Data
LT1200012


--> Instructions & Details <--

> Programming Language:
Python (v3.8.5)



> STEP 1: Create the Data File ("data/dataToIndex.txt")

usage: createData.py [-h] [-k K] [-n N] [-d D] [-m M] [-l L]
optional arguments:
  -h, --help  show this help message and exit
  -k K        Key list textfile (default: "data/keyFile.txt")
  -n N        Number of lines (default: 10)
  -d D        Maximum level of nesting (default: 3)
  -m M        Maximum number of keys / each value (default: 4)
  -l L        Maximum length of string value (default: 9)



> STEP 2: Start the servers - Store Data - Run Queries

usage: kvBroker.py [-h] [-s S] [-i I] [-k K]
optional arguments:
  -h, --help  show this help message and exit
  -s S        Server ip-port list (default: "data/serverFile.txt")
  -i I        Data to store (default: "data/dataToIndex.txt")
  -k K        Pick random k servers (default: 2)
