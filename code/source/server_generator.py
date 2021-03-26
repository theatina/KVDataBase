import re 
import socket
import threading
import kvServer_funs as kvsf
import customExceptions as ce

class Server_Generator:
    
    def __init__(self,ip,port):
        # self.id = id_num
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
                while True:
                    data = conn.recv(2048)
                    data_str = data.decode()
                    # print(f"port {self.port} receives '{data_str}'")
                    if not data:
                        break

                    if "exit" in data_str:
                        print(f"\n{self.ip}:{self.port} : Bye Bye world..")
                        conn.sendall(b"RIP")
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()
                        exit()
                
                    try:
                        data_row = data_str.split(" ",maxsplit=1)
                        print(data_row)
                        if len(data_row)<2:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                        # print(data_row)
                        command = re.findall(r"[A-Z]+",data_row[0])[0]
                        # print(command)
                        if command == "PUT":
                            kvsf.PUT_query(data_row[1],trie_server_dict)
                        elif command == "GET":
                            kvsf.GET_query(data_row[1],trie_server_dict)
                        elif command == "DELETE":
                            kvsf.DELETE_query(data_row[1],trie_server_dict)
                        elif command == "QUERY":
                            kvsf.QUERY_query(data_row[1],trie_server_dict)
                        else:
                            raise ce.QueryError(f"\nError: Request ' {data_str} ' is not valid\n")
                            # continue
                    
                        
                    
                        conn.sendall(b"OK")
                        # if "exit" in data_str:
                        #     print(f"\nExiting world..\n")
                        #     conn.shutdown(socket.SHUT_RDWR)
                        #     conn.close()
                        #     return 9
                        
                    except ce.QueryError as err:
                        print(f"\nServer {self.ip}:{self.port} : {err.args[0]}")
                        conn.sendall(b"Problem")
                    
                    
            
            
