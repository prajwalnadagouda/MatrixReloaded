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
import time

class peer:
    server_connection=0
    peers_assigned=0
    p=0

    def start_compute(self,X,Y):
        X=ast.literal_eval(X)
        Y=ast.literal_eval(Y)
        print("123456789",X,Y)
        config = configparser.ConfigParser()
        config.read('info.ini')
        peers=self.peers_assigned
        print("start compute")
        print(peers)
        peer_connections=[]
        lock_connections={}
        for peer in peers:
            peer_connections.append((peer[0],peers[peer]))
            lock_connections[peers[peer]]=0

        def parallel_calls(lock_connections,sdic, num, host1, port1,X,Y):
            # return str(lock_connections)+"-"+str(sdic)+"-"+str(num)+"-"+str(connection1)+"-"+str(X)+str(Y)
            print('Waiting for peer connection response')
            print((host1, port1))
            while lock_connections[port1]:
                    pass
            try:
                peer_connect = socket.socket()
                peer_connect.connect((host1, int(port1)))
            except socket.error as e:
                print(str(e))
            
            res = peer_connect.recv(8192)
            res = res.decode('utf-8')
            if(res=="Approved by peer"):
                peer_connect.send(bytes(str(X), 'utf-8'))
                ans=peer_connect.recv(8192)
                peer_connect.send(bytes(str(Y), 'utf-8'))
                ans=peer_connect.recv(8192)
                ans=ans.decode('utf-8')
                peer_connect.send(bytes("done", 'utf-8'))
                print(ans)
                sdic[num]=ans
                peer_connect.close()
            # lock_connections[port1]=0
            return sdic


        def strassen_algorithm(lock_connections,peer_connections, x, y):
            x=np.array(x)
            y=np.array(y)
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
            # return str(peer_connections)
            print("peer count",peer_count)
            list1=[a,a+b,c+d,d,a+d,b-d,a-c]
            list2=[f-h,h,e,g-e,e+h,g+h,e+f]
            print("list1",list1)
            print("list2",list2)
            # return str(peer_connections)
            for temp in range(1,8):
                peer_turn_ip=peer_connections[temp%peer_count][0]
                peer_turn_port=peer_connections[temp%peer_count][1]
                processThread = Thread(target=parallel_calls, args=(lock_connections, sdic, temp, peer_turn_ip, peer_turn_port,list1[temp-1].tolist(), list2[temp-1].tolist()))
                processThread.start()
                # return parallel_calls(lock_connections, sdic, temp,peer_turn,list1[temp-1].tolist(), list2[temp-1].tolist())
            # sleep(1)
            # return str(sdic)
            while(len(sdic)!=7):
                pass

            print("done")
            # return str(sdic)
            for i in sdic:
                sdic[i]=np.array(ast.literal_eval(sdic[i]))
            # return str(sdic)

            result = np.zeros((2 * m, 2 * m), dtype=np.int32)
            result[: m, : m] = sdic[5] + sdic[4] - sdic[2] + sdic[6]
            result[: m, m:] = sdic[1] + sdic[2]
            result[m:, : m] = sdic[3] + sdic[4]
            result[m:, m:] = sdic[1] + sdic[5] - sdic[3] - sdic[7]
            return str(result[: n, : n].tolist())
        def strassen_traditional(x, y):
            
            result = []
            for i in range(len(x)):
                temp =[]
                for j in range(len(y)):
                    temp.append(0)
                result.append(temp)

            for i in range(len(x)):
                 for j in range(len(y[0])):
                    for k in range(len(y)):
                        result[i][j] += x[i][k] * y[k][j]


        start_time = time.time()
        ans_trad=strassen_traditional(X,Y)
        end_time = (time.time())
        total_time_trad= (end_time-start_time)
        start_time = time.time()
        ans=strassen_algorithm(lock_connections,peer_connections,X,Y)
        end_time = time.time()
        total_time = (end_time-start_time)/10

        ans = {
            "ans" :str(ans),
            "time_taken" :total_time,
            "time_taken_trad":total_time_trad
        }
        return ans

    def fetch_peers(self):
        server=self.server_connection
        print("we are about to start computing")
        Input = "PEER-DETAILS"
        server.send(str.encode(Input))
        res = server.recv(8192)
        res = res.decode('utf-8')
        res = ast.literal_eval(res)
        self.peers_assigned=res
        return str(res)

    def server_communication(self,ClientMultiSocket):
        while True:
            # Input = input('Hey there: ')
            sleep(100)
            Input = "P"
            ClientMultiSocket.send(str.encode(Input))
            res = ClientMultiSocket.recv(8192)
            # print(res.decode('utf-8'))
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
        res = ClientMultiSocket.recv(8192)
        if(res.decode('utf-8')=="Processing"):
            print("Peer addition is under process")
        else:
            print("Couldn't connect. Please retry later")
            return
        Input=config['self']['ip']
        ClientMultiSocket.send(bytes(Input, 'utf-8'))

        testmat1 = ClientMultiSocket.recv(8192)
        testmat1 = ast.literal_eval((testmat1.decode('utf-8')))
        ClientMultiSocket.send(bytes("Got", 'utf-8'))
        testmat2 = ClientMultiSocket.recv(8192)
        testmat2 = ast.literal_eval((testmat2.decode('utf-8')))
        reply=peer.peer_calculation(self,testmat1,testmat2)
        reply=str.encode(str(reply.tolist()))
        ClientMultiSocket.send((reply))
        approvalresponse = ClientMultiSocket.recv(8192)
        print(approvalresponse.decode('utf-8'))
        Input=config['ports']['2008']
        ClientMultiSocket.send(bytes(Input, 'utf-8'))
        res = ClientMultiSocket.recv(8192)
        self.server_connection=ClientMultiSocket
        peer.server_communication(self,ClientMultiSocket)
        
    
    def peer_calculation(self,x, y):
        x=np.array(x)
        y=np.array(y)
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
        p1 = self.peer_calculation(a, f - h)
        p2 = self.peer_calculation(a + b, h)
        p3 = self.peer_calculation(c + d, e)
        p4 = self.peer_calculation(d, g - e)
        p5 = self.peer_calculation(a + d, e + h)
        p6 = self.peer_calculation(b - d, g + h)
        p7 = self.peer_calculation(a - c, e + f)
        result = np.zeros((2 * m, 2 * m), dtype=np.int32)
        result[: m, : m] = p5 + p4 - p2 + p6
        result[: m, m:] = p1 + p2
        result[m:, : m] = p3 + p4
        result[m:, m:] = p1 + p5 - p3 - p7
        return result[: n, : n-1]

    def peer_compute(self):
        config = configparser.ConfigParser()
        config.read('info.ini')
        ClientMultiSocket = socket.socket()
        host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        print(host)
        port = 2008
        thread_count = 0
        try:
            ClientMultiSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Socket is listening for peers..')
        ClientMultiSocket.listen(5)
        while True:
            Client, address = ClientMultiSocket.accept()
            print("connected to",Client)
            try:
                Client.sendall(b"Approved by peer")
                X = Client.recv(8192)
                X = X.decode('utf-8')
                X = ast.literal_eval((X))
                Client.sendall(str.encode("M1"))
                Y = Client.recv(8192)
                Y = Y.decode('utf-8')
                Y = ast.literal_eval((Y))
                Client.sendall(str.encode(str(self.peer_calculation(X,Y).tolist())))
                # connection.sendall(str.encode(str(Y)))
                stat = Client.recv(8192)
                # print("y->",X+Y)
            except:
                continue
                print("connection closed")
            Client.close()
            # multi_threaded_client(Client,address)
        # start_new_thread(multi_threaded_client, (Client, address))
        ClientMultiSocket.close()

    
    def peer_starter():
        # return "asa"
        peer_tracker = Thread(target=p.connect_server, daemon=True, name='peer tracker')
        peer_tracker.start()
        wasss = Thread(target=p.peer_compute, daemon=True, name='hello boy')
        wasss.start()
        sleep(5)
        peer_tracker.join()
        wasss.join()

    def cal_starter(X,Y):
        p.fetch_peers()
        ans = p.start_compute(X,Y)
        print(ans)
        # print(total_time)
        return p.start_compute(X,Y)

p= peer()