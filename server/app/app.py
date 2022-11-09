import server
from flask import Flask, render_template
from threading import Thread


app = Flask(__name__)

@app.route('/')
def hello():
    return 'This Compose/Flask demo has been viewed time(s)'

@app.route('/start')
def start():
    # peer_tracker = Thread(target=server.peer_tracker, daemon=True, name='peer tracker')
    starting= Thread(target=server.server.starter(), daemon=True, name='distribute work')
    starting.start()
    starting.join()
    return render_template('hello.html', name = "Connected")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)