import peer
from flask import Flask, render_template, request
import json
from threading import Thread

app = Flask(__name__)

@app.route('/')
def hello():
    return 'This Compose/Flask demo has been viewed time(s)'

@app.route('/calstart')
def calstart():
    # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
    # starting= Thread(target=peer.peer.starter(), daemon=True, name='distribute work')
    # starting.start()
    # starting.join()
    # return("wassup")
    return(peer.peer.cal_starter())
    # return render_template('index.html', name = "Connected")

@app.route('/peerstart')
def start():
    # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
    # starting= Thread(target=peer.peer.starter(), daemon=True, name='distribute work')
    # starting.start()
    # starting.join()
    # return("wassup")
    return(peer.peer.peer_starter())

@app.route('/connect')
def connect_server():
    print("hiiiiii")
    return render_template('index.html', name = "Connected")

@app.route('/connected', methods = ['POST', 'GET'])
def connect():
    print ("adasdas")
    # print(list(request))
    data = request.get_json()
    X=data['firstMatrix']
    Y=data['secondMatrix']
    if request.method == "POST":
        val=(peer.peer.cal_starter(X,Y))
        print("bhai")
        print(val)
        # return val
        return json.dumps(val)
    return "hi"

if __name__ == "__main__":
    peer_starter = Thread(target=peer.peer.peer_starter, daemon=True, name='peer tracker')
    peer_starter.start()
    app.run(host="0.0.0.0", debug=True)
    peer_starter.join()
