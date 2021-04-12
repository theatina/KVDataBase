import re
import json

def silly_parser(val):
    temp_d = {}
    print(val)
    if len(val)==1 or val=="{}":  
        return val
    
    elif val!="{}":
        val_tokens = val.split(" ")
        temp_key = ""
        
        pos = 0
        while pos!=len(val_tokens):
            if val_tokens[pos]=="{" or val_tokens==";":
                pos+=1
                temp_key=val_tokens[pos]
                pos+=1
            
            # elif val_tokens[pos]==":":
                pos+=1
                # if val_tokens[pos]=="{":
                temp_d[temp_key] = silly_parser(" ".join(val_tokens[pos:]))
                pos+=1
                # else:
                    #     temp_d[temp_key] = val_tokens[pos]
            
            # elif val_tokens[pos]=="}" and val_tokens[pos-1]!="{":
            #     return temp_d
            else:
                return val_tokens[pos]
            
            # pos+=1

            
                
        

    return temp_d 



def json_to_dict(data):
    temp_data_dict = {}
    print(data)
    if data!="{}":
        if ";" in data:
            data = re.sub(";", ",", data)
            # print(data)
        
        top_level_key,tlk_value = data.split(" : ", maxsplit=1)
        # print(f"\nBefore:\nTLK: {top_level_key}\nValue: {tlk_value}\n")
        # val = tlk_value.split(" ")
        # print(val)
        # print(tlk_value)
        temp_data_dict[top_level_key] = json.loads(tlk_value)

    return temp_data_dict




# string = '"key1" : { "height" : { "age" : 99 ; "postal_code" : {} } }'
# data_dict = json.loads( string)
# print(data_dict["key1"]["height"]["age"])
# exit()

# string2 = '"key2" : {}'

with open("../data/dataToIndex.txt","r",encoding="utf-8") as r:
    lines = r.readlines()
    
    for s in lines:
        data_dict = json_to_dict(s)
        # data_dict2 = json_to_dict(string2)
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
