import socket
import os
from _thread import *
from time import sleep
from multiprocessing import Process
import sys
from threading import Thread

class server:
    def __init__():
        pass

    def peer_tracker():
        peer_list=[]
        ServerSideSocket = socket.socket()
        host = '172.60.0.2'
        # host = '127.0.0.1'
        port = 2006
        thread_count = 0
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
            pass
        print('Socket is listening..')
        ServerSideSocket.listen(5)
        def multi_threaded_client(connection,address):
            connection.send(str.encode('Server is working:'))
            while True:
                try:
                    data = connection.recv(2048)
                    response = 'Server message: ' + data.decode('utf-8')
                    if not data:
                        break
                    connection.sendall(str.encode(response))
                except:
                    print("connection closed")
            connection.close()
            peer_list.remove(address)
            print(peer_list)
        while True:
            Client, address = ServerSideSocket.accept()
            peer_list.append(address)
            Client.sendall(b"Approved")
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (Client, address))
            thread_count += 1
            print('Thread Number: ' + str(thread_count))
            print(peer_list)
            # break
        ServerSideSocket.close()
    
#     def peer_work_distributer():
#         pass
    def starter():
        server.peer_tracker()
        # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
        # peer_tracker.start()
        # # wasss = Thread(target=server.peer_work_distributer, daemon=True, name='distribute work')
        # # wasss.start()

        # peer_tracker.join()
# wasss.join()

# server.start()