import socket
import threading

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

    def startserver(self):
        print(f"\nServer: Hi, my ip is: {self.ip} and port: {self.port}")
        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()

            with conn:
                print(f"Server with ip '{self.ip}' and port '{self.port}': Connected by", addr)
                while True:
                    data = conn.recv(1024)
                    data_str = data.decode()
                    print(f"port {self.port} receives '{data_str}'")
                    if not data:
                        break
                    
                    conn.sendall(data)
                    if "exit" in data_str:
                        print(f"\nExiting world..\n")
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()
                        return 9
                    
                    
            
            
