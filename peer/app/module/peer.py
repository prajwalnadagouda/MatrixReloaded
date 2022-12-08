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
    def __init__(self) -> None:
        self.peer_count=0
        self.peer_connections=[]
        
    def start_compute(self,X,Y):
        X=ast.literal_eval(X)
        Y=ast.literal_eval(Y)
        #print("123456789",X,Y)
        const1=1
        const2=0.1
        config = configparser.ConfigParser()
        config.read('info.ini')
        peers=self.peers_assigned
        print("start compute")
        print(peers)
        self.peer_connections=[]
        lock_connections={}
        for peer in peers:
            self.peer_connections.append((peer[0],peers[peer]))
            lock_connections[peers[peer]]=0
        print("peer lock intilization",lock_connections)
        def parallel_calls(lock_connections,sdic, num, host1, port1,X,Y):
            print('Waiting for peer connection response',num)
            print((host1, port1))
            while lock_connections[port1]:
                print("lock dictionary",lock_connections)
                pass
            try:
                peer_connect = socket.socket()
                peer_connect.connect((host1, int(port1)))
                # lock_connections[port1]=1
            except socket.error as e:
                print("tech redo",str(e))
                del self.peer_connections[num%self.peer_count]
                self.peer_count-=1
                sdic[num]="tech redo"
            try:
                print("try to -",num)
                res = peer_connect.recv(1024)
                res = res.decode('utf-8')
                stand = "pass"
                if(res=="Approved by peer"):
                    strX=str(X)
                    xlength=len(strX)
                    peer_connect.sendall(bytes(str(xlength), 'utf-8'))
                    # peer_connect.recv(1024)
                    xloop=0
                    while xlength > 0:
                        peer_connect.recv(1024)
                        peer_connect.sendall(bytes(strX[xloop*1024:(xloop+1)*1024], 'utf-8'))
                        xlength-=1024
                        xloop+=1

                    ans=peer_connect.recv(1024)

                    strY=str(Y)
                    ylength=len(strY)
                    peer_connect.sendall(bytes(str(ylength), 'utf-8'))
                    # peer_connect.recv(1024)
                    yloop=0
                    while ylength > 0:
                        peer_connect.recv(1024)
                        peer_connect.sendall(bytes(strY[yloop*1024:(yloop+1)*1024], 'utf-8'))
                        ylength-=1024
                        yloop+=1
                    peer_connect.recv(1024)
                    peer_connect.sendall(bytes("done", 'utf-8'))
                    lens= int(peer_connect.recv(1024).decode('utf-8'))
                    print(num,"find this -",lens)
                    peer_connect.sendall(bytes("done", 'utf-8'))
                    ans=''
                    while(lens >0):
                        ans1 = peer_connect.recv(1024).decode('utf-8')
                        peer_connect.sendall(bytes("done", 'utf-8'))   
                        ans += ans1
                        lens-=1024
                        #print("lens---",lens,ans1)
                    #print("ohooo",ans)
                    # peer_connect.sendall(bytes("done", 'utf-8'))
                    sdic[num]=ans
                    peer_connect.close()
                    lock_connections[port1]=0
            except:
                sdic[num]="redo"
            return sdic


        def strassen_algorithm(lock_connections, x, y):
            x=np.array(x)
            y=np.array(y)
            #print(x,y)
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
            self.peer_count=len(self.peer_connections)
            # return str(peer_connections)
            list1=[a,a+b,c+d,d,a+d,b-d,a-c]
            list2=[f-h,h,e,g-e,e+h,g+h,e+f]
            # return str(peer_connections)
            temp=1
            print("peer count",self.peer_count)
            while(temp < 8):
                a=[]
                for i in range(self.peer_count):
                    peer_turn_ip=self.peer_connections[temp%self.peer_count][0]
                    peer_turn_port=self.peer_connections[temp%self.peer_count][1]
                    processThread = Thread(target=parallel_calls, args=(lock_connections, sdic, temp, peer_turn_ip, peer_turn_port,list1[temp-1].tolist(), list2[temp-1].tolist()))
                    print("thread-",processThread)
                    a.append(processThread)
                    processThread.start()
                    print(temp,a)
                    temp+=1
                    if(temp>7):
                        break
                for j in a:
                    j.join()
                    print("loop-",j)
                print("hahha")



            # for temp in range(1,8):
            #     peer_turn_ip=self.peer_connections[temp%self.peer_count][0]
            #     peer_turn_port=self.peer_connections[temp%self.peer_count][1]
            #     processThread = Thread(target=parallel_calls, args=(lock_connections, sdic, temp, peer_turn_ip, peer_turn_port,list1[temp-1].tolist(), list2[temp-1].tolist()))
            #     processThread.start()
            #     processThread.join()
                
            while(len(sdic)!=7):
                try:
                    pass
                    # print("fixing few things")
                    # failedcal=int(list(sdic.keys()) [list(sdic.values()).index("redo")])
                    # del sdic[str(failedcal)]
                    # peer_turn_ip=self.peer_connections[failedcal%self.peer_count][0]
                    # peer_turn_port=self.peer_connections[failedcal%self.peer_count][1]
                    # processThread = Thread(target=parallel_calls, args=(lock_connections, sdic, failedcal, peer_turn_ip, peer_turn_port,list1[failedcal-1].tolist(), list2[failedcal-1].tolist()))
                    # processThread.start()
                except:
                    pass
            print("done")
            #print("this is so done",sdic)
            for i in sdic:
                sdic[i]=np.array(ast.literal_eval(sdic[i]))

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
        total_time_trad= (end_time-start_time)*const1
        start_time = time.time()
        ans=strassen_algorithm(lock_connections,X,Y)
        end_time = time.time()
        total_time = (end_time-start_time)*const2

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
        server.sendall(str.encode(Input))
        res = server.recv(1024)
        res = res.decode('utf-8')
        res = ast.literal_eval(res)
        self.peers_assigned=res
        return str(res)

    def server_communication(self,ClientMultiSocket):
        while True:
            sleep(100)
            Input = "P"
            ClientMultiSocket.sendall(str.encode(Input))
            res = ClientMultiSocket.recv(1024)
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
        if(res.decode('utf-8')=="Processing"):
            print("Peer addition is under process")
        else:
            print("Couldn't connect. Please retry later")
            return
        Input=config['self']['ip']
        ClientMultiSocket.sendall(bytes(Input, 'utf-8'))

        testmat1 = ClientMultiSocket.recv(1024)
        testmat1 = ast.literal_eval((testmat1.decode('utf-8')))
        ClientMultiSocket.sendall(bytes("Got", 'utf-8'))
        testmat2 = ClientMultiSocket.recv(1024)
        testmat2 = ast.literal_eval((testmat2.decode('utf-8')))
        reply=peer.peer_calculation(self,testmat1,testmat2)
        reply=str.encode(str(reply.tolist()))
        ClientMultiSocket.sendall((reply))
        approvalresponse = ClientMultiSocket.recv(1024)
        print(approvalresponse.decode('utf-8'))
        Input=config['ports']['2008']
        ClientMultiSocket.sendall(bytes(Input, 'utf-8'))
        res = ClientMultiSocket.recv(1024)
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
        return result[: n, : n]

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
            # try:
            Client, address = ClientMultiSocket.accept()
            print("connected to",Client)
            Client.sendall(b"Approved by peer")
            lenx = int(Client.recv(1024).decode('utf-8'))
            Client.sendall(bytes("pass",'utf-8'))
            X=''
            while lenx >0:
                X1 = Client.recv(1024).decode('utf-8')
                Client.sendall(bytes("done", 'utf-8'))
                X += X1
                lenx-=1024
            X = ast.literal_eval((X))
            # Client.sendall(bytes("pass",'utf-8'))
            leny = int(Client.recv(1024).decode('utf-8'))
            Client.sendall(bytes("pass",'utf-8'))
            #print("X works")
            Y=''
            while leny >0:
                Y1 = Client.recv(1024).decode('utf-8')
                Client.sendall(bytes("done", 'utf-8'))
                Y += Y1
                leny-=1024
            Y = ast.literal_eval((Y))
            Client.recv(1024)
            #print("This is the matrix",X,Y)
            solution=self.peer_calculation(X,Y).tolist()
            solution=str(solution)
            solutionlength=len(solution)
            #print("real ans",solution)
            Client.sendall(bytes(str(solutionlength), 'utf-8'))
            iloop=0
            while solutionlength > 0:
                Client.recv(1024)
                Client.sendall(bytes(solution[iloop*1024:(iloop+1)*1024], 'utf-8'))
                #print("split up",solution[iloop*1024:(iloop+1)*1024])
                solutionlength-=1024
                iloop+=1
            stat = Client.recv(1024)
            Client.close()
            # except Exception as e:
            #     print("I am doing some reacceptance",e)
            #     continue
        ClientMultiSocket.close()

    
    def peer_starter():
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
        return p.start_compute(X,Y)

p= peer()