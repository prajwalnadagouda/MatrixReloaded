import socket
import os
from _thread import *
from time import sleep
from multiprocessing import Process
import sys
from threading import Thread

class server:
    peer_dict={}
    peer_availability={}

    def multi_threaded_client(self,connection,address):
        connection.send(str.encode('Server is working:'))
        while True:
            try:
                data = connection.recv(2048)
                data = data.decode('utf-8')
                response = 'Server message: ' + data
                if not data:
                    break
                print(response)
                if(data == "PEER-DETAILS"):
                    print("Sharing details of a max of 7 peers")
                    res={}
                    count=0
                    for i in self.peer_availability:
                        res[i]=self.peer_availability[i]
                        count+=1
                        if(count==7):
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
        self.peer_availability.pop(address)
        print("gone")
        print(self.peer_dict)

    def accept_peer(self):
        ServerSideSocket = socket.socket()
        host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        print(host)
        port = 2006
        thread_count = 0
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        ServerSideSocket.listen(5)
        while True:
            Client, address = ServerSideSocket.accept()
            Client.sendall(b"Approved")
            ip = Client.recv(2048)
            ip = ip.decode('utf-8')
            Client.sendall(b"Approved")
            port = Client.recv(2048)
            port = port.decode('utf-8')
            self.peer_dict[(ip,address[1])]=port
            self.peer_availability[(ip,address[1])]=port
            address=(ip,address[1])
            print(self.peer_dict)
            print(self.peer_availability)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(server.multi_threaded_client, (self, Client, address))
            thread_count += 1
            print('Thread Number: ' + str(thread_count))
        ServerSideSocket.close()

    def starter():
        s= server()
        s.accept_peer()

# class server:
#     def __init__():
#         pass

#     def peer_tracker():
#         peer_list=[]
#         ServerSideSocket = socket.socket()
#         host = '172.60.0.2'
#         # host = '127.0.0.1'
#         port = 2006
#         thread_count = 0
#         try:
#             ServerSideSocket.bind((host, port))
#         except socket.error as e:
#             print(str(e))
#             pass
#         print('Socket is listening..')
#         ServerSideSocket.listen(5)
#         def multi_threaded_client(connection,address):
#             connection.send(str.encode('Server is working:'))
#             while True:
#                 try:
#                     data = connection.recv(2048)
#                     response = 'Server message: ' + data.decode('utf-8')
#                     if not data:
#                         break
#                     connection.sendall(str.encode(response))
#                 except:
#                     print("connection closed")
#             connection.close()
#             peer_list.remove(address)
#             print(peer_list)
#         while True:
#             Client, address = ServerSideSocket.accept()
#             peer_list.append(address)
#             Client.sendall(b"Approved")
#             print('Connected to: ' + address[0] + ':' + str(address[1]))
#             start_new_thread(multi_threaded_client, (Client, address))
#             thread_count += 1
#             print('Thread Number: ' + str(thread_count))
#             print(peer_list)
#             # break
#         ServerSideSocket.close()
    
#     def starter():
#         s= server()
#         s.accept_peer()    

        # peer_tracker.join()
# wasss.join()

# server.start()