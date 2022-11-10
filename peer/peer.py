import socket
from _thread import *
from threading import Thread
from time import sleep
import configparser
import socket
import sys
# print(([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))



class peer:
    def server_communication(ClientMultiSocket):
        while True:
            Input = input('Hey there: ')
            ClientMultiSocket.send(str.encode(Input))
            res = ClientMultiSocket.recv(1024)
            print(res.decode('utf-8'))
        ClientMultiSocket.close()

    def connect_server():
        config = configparser.ConfigParser()
        config.read('info.ini')
        ClientMultiSocket = socket.socket()
        host = str(config['host']['id'])
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
        Input=config['ports']['5000']
        ClientMultiSocket.send(bytes(Input, 'utf-8'))
        res = ClientMultiSocket.recv(1024)
        peer.server_communication(ClientMultiSocket)
        

    def peer_to_peer():
        return
        peer_list=[]
        ServerSideSocket = socket.socket()
        host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        print(host)
        port = 2008
        thread_count = 0
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Peer Socket is listening..')
        ServerSideSocket.listen(5)
        def multi_threaded_client(connection,address):
            connection.send(str.encode('Server is working:'))
            while True:
                try:
                    data = connection.recv(2048)
                    response = 'Peer Server message: ' + data.decode('utf-8')
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

    def matrix_multiplier():
        pass

def wassup():
    while True:
        print("going to sleep")
        sleep(20)

peer_tracker = Thread(target=peer.connect_server, daemon=True, name='peer tracker')
peer_tracker.start()
wasss = Thread(target=peer.peer_to_peer, daemon=True, name='hello boy')
wasss.start()

peer_tracker.join()
wasss.join()