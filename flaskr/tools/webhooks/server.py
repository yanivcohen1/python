import time
from flask import Flask, Response, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def event_stream():
    # while True:
        time.sleep(1)
        yield 'data: The time is now {}\n\n'.format(time.ctime())

@app.route('/events')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
