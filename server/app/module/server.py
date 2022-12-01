import socket
import os
from _thread import *
from time import sleep
from multiprocessing import Process
import sys
from threading import Thread
import json
import ast
from random import randrange

class server:
    thread_count = 0
    peer_dict={}
    peer_availability={}
    def __init__(self):
        pass

    def peer_communication(self,connection,address):
        connection.send(str.encode('Server is working:'))
        while True:
            try:
                data = connection.recv(2048)
                data = data.decode('utf-8')
                response = 'Server message: ' + data
                if not data:
                    break
                # print(response)
                if(data == "PEER-DETAILS"):
                    print("Sharing details of a max of 7 peers")
                    res={}
                    count=0
                    for i in self.peer_availability:
                        res[i]=self.peer_availability[i]
                        # self.peer_availability.pop(i)
                        count+=1
                        if(count==8):
                            break
                    response=str(res)
                    print(response)
                    connection.sendall((str.encode(response)))
                else:
                    connection.sendall(str.encode(response))
            except:
                print("connection closed")
        connection.close()
        self.peer_dict.pop(address)
        try:
            self.peer_availability.pop(address)
        except:
            pass
        self.thread_count-=1
        print("A peer has exited. Current number of peers are-",self.thread_count,"\n")

        print(self.peer_dict)


    def accept_peer(self):
        ServerSideSocket = socket.socket()
        # host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        host = "0.0.0.0"
        print(host)
        port = 2006
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        ServerSideSocket.listen(5)
        while True:
            Client, address = ServerSideSocket.accept()
            Client.sendall(b"Processing")
            ip = Client.recv(2048)
            ip = ip.decode('utf-8')

            #send test matrix 
            randint=randrange(10)
            m1=[[randint,randint],[randint,randint]]
            Client.sendall(bytes(str(m1), 'utf-8'))
            A = Client.recv(2048)
            Client.sendall(bytes(str(m1), 'utf-8'))
            res = Client.recv(2048)
            res = ast.literal_eval(res.decode('utf-8'))
            testvar=2*(randint**2)
            m2=[[testvar,testvar],[testvar,testvar]]
            print("Expected-",m2)
            print("Received-",res)
            
            if(m2==res):
                print("This peer will be approved")
                Client.sendall(b"Approved")
            else:
                print("This peer will be rejected")
                Client.sendall(b"Rejected")
                continue
            port = Client.recv(2048)
            port = port.decode('utf-8')
            self.peer_dict[(ip,address[1])]=port
            self.peer_availability[(ip,address[1])]=port
            address=(ip,address[1])

            print(self.peer_dict)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(server.peer_communication, (self, Client, address))
            self.thread_count += 1
            print('Peer Number: ' + str(self.thread_count),"\n")
        ServerSideSocket.close()

    def starter():
        s= server()
        s.accept_peer()

s= server()
s.accept_peer()