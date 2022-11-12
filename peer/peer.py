import socket
from _thread import *
from threading import Thread
from time import sleep
import configparser
import socket
import sys
import json
import ast
import numpy as np

# print(([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))



class peer:
    server_connection=0
    peers_assigned=0

    def start_compute(self):
        config = configparser.ConfigParser()
        peers=self.peers_assigned
        print("start compute")
        print(peers)
        peer_connections=[]
        lock_connections={}
        for peer in peers:
            print(peer[0])
            print(peers[peer])
            peer_connect=socket.socket()
            host = peer[0]
            port = int(peers[peer])
            print('Waiting for peer connection response')
            print((host, port))
            try:
                peer_connect.connect((host, port))
                peer_connections.append(peer_connect)
                lock_connections[peer_connect]=0
            except socket.error as e:
                print(str(e))

        def parallel_calls(lock_connections,sdic, num,connection,X,Y):
            print("1->",num)
            sleep(2)
            print("2->",num)
            while lock_connections[connection]:
                    pass
            lock_connections[connection]=1
            res = connection.recv(1024)
            res = res.decode('utf-8')
            print("info -",res)
            if(res=="Approved by peer"):
                connection.send(bytes(str(X)+str(Y), 'utf-8'))
                ans=connection.recv(2048)
                ans=ans.decode('utf-8')
                connection.send(bytes("bye", 'utf-8'))
                print(ans)
                sdic[num]=ans
            lock_connections[connection]=0
            

        def strassen_algorithm(lock_connections,peer_connections, x, y):
            print(x,y)
            sdic={}
            if x.size == 1 or y.size == 1:
                return x * y
            n = x.shape[0]
            if n % 2 == 1:
                x = np.pad(x, (0, 1), mode='constant')
                y = np.pad(y, (0, 1), mode='constant')
            m = int(np.ceil(n / 2))
            a = x[: m, : m]
            b = x[: m, m:]
            c = x[m:, : m]
            d = x[m:, m:]
            e = y[: m, : m]
            f = y[: m, m:]
            g = y[m:, : m]
            h = y[m:, m:]
            peer_count=len(peer_connections)
            print("peer count",peer_count)
            list1=[a,a+b,c+d,d,a+d,b-d,a-c]
            list2=[f-h,h,e,g-e,e+h,g+h,e+f]
            print("list1",list1)
            print("list2",list2)
            
            for temp in range(1,8):
                peer_turn=peer_connections[temp%peer_count]
                # start_new_thread(parallel_calls, (lock_connections, sdic, temp,peer_turn,a, f - h))
                processThread = Thread(target=parallel_calls, args=(lock_connections, sdic, temp,peer_turn,list1[temp-1], list2[temp-1]))
                processThread.start()
            
            while(len(sdic)!=7):
                pass

            print("done")
            print(sdic)
            return "pass"
            
            result = np.zeros((2 * m, 2 * m), dtype=np.int32)
            result[: m, : m] = sdic[5] + sdic[4] - sdic[2] + sdic[6]
            result[: m, m:] = sdic[1] + sdic[2]
            result[m:, : m] = sdic[3] + sdic[4]
            result[m:, m:] = sdic[1] + sdic[5] - sdic[3] - sdic[7]
            print(result[: n, : n])
            return "pass"

        X=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        Y=np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
        ans=strassen_algorithm(lock_connections,peer_connections,X,Y)
        print(ans)

    def fetch_peers(self):
        server=self.server_connection
        print("we are about to start computing")
        Input = "PEER-DETAILS"
        server.send(str.encode(Input))
        res = server.recv(1024)
        res = res.decode('utf-8')
        res = ast.literal_eval(res)
        self.peers_assigned=res
        print(res)

    def server_communication(self,ClientMultiSocket):
        while True:
            Input = input('Hey there: ')
            ClientMultiSocket.send(str.encode(Input))
            res = ClientMultiSocket.recv(1024)
            print(res.decode('utf-8'))
        ClientMultiSocket.close()

    def connect_server(self):
        config = configparser.ConfigParser()
        config.read('info.ini')
        ClientMultiSocket = socket.socket()
        host = str(config['host']['ip'])
        port = 2006
        print('Waiting for connection response')
        try:
            ClientMultiSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
        res = ClientMultiSocket.recv(1024)
        print(res)
        if(res.decode('utf-8')=="Approved"):
            print("Peer added to the list")
        else:
            print("Couldn't connect. Please retry later")
            return
        Input=config['self']['ip']
        ClientMultiSocket.send(bytes(Input, 'utf-8'))
        res = ClientMultiSocket.recv(1024)
        Input=config['ports']['2008']
        ClientMultiSocket.send(bytes(Input, 'utf-8'))
        res = ClientMultiSocket.recv(1024)
        self.server_connection=ClientMultiSocket
        peer.server_communication(self,ClientMultiSocket)
        

    def peer_compute(self):
        # return
        config = configparser.ConfigParser()
        config.read('info.ini')
        ClientMultiSocket = socket.socket()
        ServerSideSocket = socket.socket()
        host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        print(host)
        port = int(config['ports']['2008'])
        thread_count = 0
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Socket is listening for peers..')
        ServerSideSocket.listen(5)
        Client, address = ServerSideSocket.accept()
        def multi_threaded_client(connection,address):
            while True:
                try:
                    Client.sendall(b"Approved by peer")
                    data = Client.recv(2048)
                    data = data.decode('utf-8')
                    # print(data)
                    connection.sendall(str.encode(data))
                    data = Client.recv(2048)
                    data = data.decode('utf-8')
                    # print(data)
                except:
                    continue
                    print("connection closed")
            connection.close()
        start_new_thread(multi_threaded_client, (Client, address))
        ServerSideSocket.close()

    def matrix_multiplier():
        pass

def wassup():
    while True:
        print("going to sleep")
        sleep(20)


p= peer()
peer_tracker = Thread(target=p.connect_server, daemon=True, name='peer tracker')
peer_tracker.start()
wasss = Thread(target=p.peer_compute, daemon=True, name='hello boy')
wasss.start()
sleep(5)
p.fetch_peers()
p.start_compute()
peer_tracker.join()
wasss.join()