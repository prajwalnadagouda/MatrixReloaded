import socket
from threading import Thread
from time import sleep

import socket
print(([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))


class peer:
    def connect_server():
        ClientMultiSocket = socket.socket()
        # host = '127.0.0.1'
        host = '10.10.10.10'
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
        while True:
            Input = input('Hey there: ')
            ClientMultiSocket.send(str.encode(Input))
            res = ClientMultiSocket.recv(1024)
            print(res.decode('utf-8'))
        # ClientMultiSocket.close()

    def peer_to_peer():
        pass

def wassup():
    while True:
        print("going to sleep")
        sleep(20)

peer_tracker = Thread(target=peer.connect_server, daemon=True, name='peer tracker')
peer_tracker.start()
wasss = Thread(target=wassup, daemon=True, name='hello boy')
wasss.start()

peer_tracker.join()
wasss.join()