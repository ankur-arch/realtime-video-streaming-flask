### Python FlaskSocketIo Realtime Video Streamer

![./demo.PNG](./demo.PNG)

---

This project acts as a boilerplate to utilize when serving realtime videos to client over websockets.

---

### Getting Started

Install required dependencies using:

```bash
pip install -r ./requirements.txt
```

Start the application using

```git
python manage.py
```

This uses flask-socketio, eventlet ( to maximize performance via utilization of websockets ).
_With the usage of eventlet, native threading functionalities don't work. Hence to process images using opencv or any image processing library of your choice. Make changes in the [get_frames.py](./get_frames.py)_

### Implementing ML code

To implement custom features such as face recognition, object detection and sending metadata along with the video stream.

##### Server-side

[get_frames.py](./get_frames.py)

```py
def generate_frame(socket: SocketIO):
    ## Change implementation to add url of realtime video feed
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

```

##### Client-side

Notice where are sending data as a dict, where **image is the frame** and **data is additional payload (it's a counter here for demonstration purposes)**

```py
data = {
            "data": count,
            "image": camera_frame
        }
```

###

This is broadcasted to all active clients via emitting an event named **stream**
[index.html](./templates/index.html)

```js
socket.on("connect", function () {
  console.log("connected");
  socket.on("stream", (data) => {
    console.log(data);
    image_element.src = data.image;
    additional_element.innerHTML = `$<h2>${data.data}</h2>`;
  });
});
```
