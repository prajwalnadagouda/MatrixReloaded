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
                data = connection.recv(4096)
                data = data.decode('utf-8')
                response = 'Server message: ' + data
                if not data:
                    break
                if(data == "PEER-DETAILS"):
                    print("Sharing details of fellow peers")
                    res={}
                    count=0
                    for i in self.peer_availability:
                        res[i]=self.peer_availability[i]
                        count+=1
                        if(count==15):
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
        host = "0.0.0.0"
        print(host)
        port = 2006
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Server is accepting peers')
        ServerSideSocket.listen(5)
        while True:
            try:
                Client, address = ServerSideSocket.accept()
                Client.sendall(b"Processing")
                ip = Client.recv(2048)
                ip = ip.decode('utf-8')
                #send test matrix 
                ri1=randrange(10)
                ri2=randrange(10)
                ri3=randrange(10)
                ri4=randrange(10)
                m1=[[ri1,ri2],[ri3,ri4]]
                Client.sendall(bytes(str(m1), 'utf-8'))
                A = Client.recv(2048)
                Client.sendall(bytes(str(m1), 'utf-8'))
                res = Client.recv(2048)
                res = ast.literal_eval(res.decode('utf-8'))
                m2=[[ri1*ri1+ri2*ri3,ri1*ri2+ri2*ri4],[ri3*ri1+ri3*ri4,ri3*ri2+ri4*ri4]]
                print("Expected result-",m2)
                print("Received response from peer-",res)
                if(m2==res):
                    print("This peer will be approved")
                    Client.sendall(b"Approved")
                else:
                    print("This peer will be rejected")
                    Client.sendall(b"Rejected")
                    continue
                #Continue with adding peer
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
            except:
                continue
        ServerSideSocket.close()

    def starter():
        s= server()
        s.accept_peer()

s= server()
s.accept_peer()