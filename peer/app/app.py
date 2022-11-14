import peer
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'This Compose/Flask demo has been viewed time(s)'

@app.route('/calstart')
def start():
    # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
    # starting= Thread(target=peer.peer.starter(), daemon=True, name='distribute work')
    # starting.start()
    # starting.join()
    # return("wassup")
    return(peer.peer.cal_starter())
    # return render_template('index.html', name = "Connected")

@app.route('/peerstart')
def calstart():
    # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
    # starting= Thread(target=peer.peer.starter(), daemon=True, name='distribute work')
    # starting.start()
    # starting.join()
    # return("wassup")
    return(peer.peer.peer_starter())

@app.route('/connect')
def connect_server():
    print("hiiiiii")
    peer.connect_server()
    return render_template('index.html', name = "Connected")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)