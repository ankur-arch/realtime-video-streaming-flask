import cv2
import base64
from time import sleep
from flask_socketio import SocketIO


def generate_frame(socket: SocketIO):
    # Change implementation to add url of realtime video feed,
    # for demo purposes a random video was used
    cap = cv2.VideoCapture('./video.mp4')
    count = 0
    while True:
        (ret, frame) = cap.read()
        if not ret:
            print('end of the video file...')
            yield None
            break
        frame = cv2.resize(frame, (400, 300))
        # Perform image processing here

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        frame = base64.b64encode(frame).decode('utf-8')
        camera_frame = "data:image/jpeg;base64,{}".format(frame)
        data = {
            "data": count,
            "image": camera_frame
        }
        count += 1
        yield (data)
        # delay
        socket.sleep(0)
