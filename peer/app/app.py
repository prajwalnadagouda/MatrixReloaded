import peer
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'This Compose/Flask demo has been viewed time(s)'

@app.route('/connect')
def connect_server():
    print("hiiiiii")
    peer.connect_server()
    return render_template('hello.html', name = "Connected")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)