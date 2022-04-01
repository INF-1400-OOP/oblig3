import socket
from _thread import start_new_thread
import pickle

class Server:
    def __init__(self, host, port, spawn_func, byterate=2048):
        self.host = host
        self.port = port
        self.br = byterate
        self.spawn_func = spawn_func

        # create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind socket
        try:
            self.s.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
        
        # listen for connections
        self.s.listen(10)
        print("[+] Server started on port " + str(self.port))

        # initialize clients and start server
        self.clients = []
        self.running = True

    def start_server(self):
        client = 0
        while self.running:
            try:

                # accept connection
                c, addr = self.s.accept()
                print("[+] Connection from: " + str(addr))
                
                # add spawned player to list
                self.clients.append(self.spawn_player())

                # start thread for client
                start_new_thread(self.handle_client, (c, addr, client))
                client += 1
            except:
                pass

    def handle_client(self, conn, addr, client):

        # send player object to client on connection
        conn.send(pickle.dumps(self.clients[client]))
        reply = ""
        while True:
            try:
                # receive player object from client
                data = pickle.loads(conn.recv(self.br))
                if not data:
                    print("[-] Client disconnected")
                    break
                else:
                    if client == 0:
                        reply = self.clients[1]
                    elif client == 1:
                        reply = self.clients[0]

                    print("[+] Received: " + str(data))
                    print("[+] Sending: " + str(reply))

                # send opponent player object back to client
                conn.sendall(pickle.dumps(reply))
            except:
                break

        print("[-] Lost connection")
        conn.close()
        self.clients.remove(conn)

    def spawn_player(self):
        return self.spawn_func()