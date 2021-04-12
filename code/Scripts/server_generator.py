import re 
import socket
import threading
import kvServer_funs as kvsf
import customExceptions as ce
import trie as tr

class Server_Generator:
    
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port)) 

        # server data 
        self.trie_dictionary = None

    def startserver(self,trie_server_dict):
        print(f"\nServer: Hi, my ip is: {self.ip} and port: {self.port}")
        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()

            with conn:
                print(f"Server with ip '{self.ip}' and port '{self.port}': Connected by", addr)
                max_buff_size = 2048
                data = conn.recv(max_buff_size)
                data_str = data.decode()
                max_buff_size = int(data_str)

                while True:
                    data = conn.recv(max_buff_size)
                    data_str = data.decode()

                    if not data:
                        break

                    if "exit" in data_str:
                        print(f"\n{self.ip}:{self.port} : Bye Bye world..")
                        conn.sendall(b"RIP")
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()
                        tr.delete_trie(trie_server_dict)
                        exit()
                
                    try:
                        data_row = data_str.split(" ",maxsplit=1)
                        
                        if len(data_row)<2:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                        
                        if "PUT" not in data_str:

                            # for i,dr in enumerate(data_row):
                            #     data_row[i] = re.sub(r"\s+", "", data_row[i])
                            # data_row = [i for i in data_row if i!=""]
                            data_row[1] = data_row[1].rstrip(" ")
                            data_row[1] = data_row[1].lstrip(" ")
                            # print(data_row)
                        
                        # data_row = data_str.split(" ",maxsplit=1)
                        # print(data_row)
                        
                        
                        # print(data_row)
                        # command = re.findall(r"[A-Z]+",data_row[0])[0]
                        command = data_row[0].rstrip(" ")
                        command = data_row[0].lstrip(" ")
                        # print(command)
                        # data_row[1] = re.sub(r"\s+","",data_row[1])
                        response = " "
                        if command == "PUT":
                            kvsf.PUT_query(data_row[1],trie_server_dict)
                        elif command == "GET":
                            response = kvsf.GET_query(data_row[1],trie_server_dict)
                            response = re.sub("'", "", response)
                        elif command == "DELETE":
                            response = kvsf.DELETE_query(data_row[1],trie_server_dict)
                        elif command == "QUERY":
                            response = kvsf.QUERY_query(data_row[1],trie_server_dict)
                            response = re.sub("'", "", response)
                        else:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                            # continue
                    
                        
                        
                        # conn.sendall(b"OK")
                        
                        # if response=={}:
                        #     data_to_send = b"NO"
                        # else:
                        data_to_send = response.encode()

                        conn.sendall(data_to_send)
                        # if "exit" in data_str:
                        #     print(f"\nExiting world..\n")
                        #     conn.shutdown(socket.SHUT_RDWR)
                        #     conn.close()
                        #     return 9
                        
                    except ce.QueryError as err:
                        print(f"\nServer {self.ip}:{self.port} : {err.args[0]}")
                        conn.sendall(b"NO")
                    
                    
            
            