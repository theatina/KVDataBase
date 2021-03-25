import re
import json

def silly_tokenizer(data):
    temp_data_dict = {}
    top_level_key,tlk_value = data.split(" : ",maxsplit=1)
    print(f"\nBefore:\nTLK: {top_level_key}\nValue: {tlk_value}\n")
    data = tlk_value.split(" ")
    print(data)

    return temp_data_dict


string = '"key1" : { "height" : { "age" : 99 ; "postal_code" : {} } }"'

data_dict = silly_tokenizer(string)
print(f"\nAfter:\n{data_dict}")


