import re

def silly_parser(val):
    temp_d = {}

    


    return temp_d 



def silly_tokenizer(data):
    temp_data_dict = {}
    top_level_key,tlk_value = data.split(" : ",maxsplit=1)
    # print(f"\nBefore:\nTLK: {top_level_key}\nValue: {tlk_value}\n")
    # val = tlk_value.split(" ")
    # print(val)

    temp_data_dict[top_level_key] = silly_parser(tlk_value)



    return temp_data_dict


string = '"key1" : { "height" : { "age" : 99 ; "postal_code" : {} } }'
string2 = '"key2" : {}'

data_dict = silly_tokenizer(string)
data_dict2 = silly_tokenizer(string2)
print(f"\nAfter:\n{data_dict}")
# print(f"\nAfter:\n{data_dict2}")








# def dict_from_string_old(val):
#     temp_d = {}
#     print(val)
#     if "{ " in val:
#         # print(val)
#         keys = val.split(" ; ")
#         for k in keys:
#             print(k)
#             temp_key,val = k.split(" : ", maxsplit=1)
#             temp_key = re.findall("\"[a-zA-Z\d]+\"",temp_key)[0]
#             val = re.sub("{","",val)
#             val = re.sub("}","",val)
#             # val = re.sub("\"","\"P",val)[0]
#             # temp_key = re.findall("\"[a-zA-Z\d]+\"",temp_key)
#             print(temp_key)
#             print(val)
#             temp_d[temp_key] = dict_from_string(val)
    
#         print(temp_d)
#     else:
#         return val
