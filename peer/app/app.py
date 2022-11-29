import peer
from flask import Flask, render_template, request
import json
from threading import Thread
import configparser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    config = configparser.ConfigParser()
    config.read('info.ini')
    val=config['ports']['5000']

    # print("hiiiiii")
    return render_template('index.html', name =val)

@app.route('/connected', methods = ['POST', 'GET'])
def connect():
    # print ("adasdas")
    # print(list(request))
    data = request.get_json()
    X=data['firstMatrix']
    Y=data['secondMatrix']
    if request.method == "POST":
        val=(peer.peer.cal_starter(X,Y))
        print(val["ans"])
        print(val["time_taken"])
        print(val)
        # return val
        return json.dumps(val)
    # return "hi"

    # return ("hiiiiii")

if __name__ == "__main__":
    peer_begin = Thread(target=peer.peer.peer_starter, daemon=True, name='peer tracker')
    peer_begin.start()
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
    peer_begin.join()
