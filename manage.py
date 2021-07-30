from flask_socketio import SocketIO, emit, send
from flask import Flask, render_template, Response, request
from time import sleep
from get_frames import generate_frame
from threading import Lock
from eventlet.green.threading import Lock


background_thread = None
background_lock = Lock()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'



socketio = SocketIO(
    app,
    always_connect=True, async_mode='eventlet',
    allowEIO4=True,
    cors_allowed_origins="*",
    logger=False,
    max_http_buffer_size=1000000,
    engineio_logger=False,
    allow_upgrades=True)


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


def task():
    global background_thread
    for res in generate_frame(socketio):
        if res is None:
            break
        socketio.emit("stream", res, broadcast=True)
    background_lock.release()
    background_thread = None
    return


@socketio.on('connect')
def connect():
    print('[INFO] Client connected: {}'.format(request.sid))
    global background_thread
    with background_lock:
        if background_thread is None:
            background_thread = socketio.start_background_task(
                target=task)


@socketio.on('disconnect')
def diconnect():
    print('A client has disconnected')


if __name__ == "__main__":
    socketio.run(app=app, host='127.0.0.1', port=3000,
                 debug=True, use_reloader=True,)
